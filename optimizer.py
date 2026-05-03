import math
from ortools.sat.python import cp_model

COGS_RATE     = 0.40
WASTE_PENALTY = 0.50
SCALE         = 1000


def optimize_production(demand_output: dict) -> dict:
    budget      = demand_output["budget"]
    donut_data  = demand_output["donut_demand"]
    drink_data  = demand_output["drink_demand"]
    user_inputs = demand_output.get("inputs", {})

    donuts = []
    for name, info in donut_data.items():
        price      = info["unit_price"]
        demand     = info["predicted_demand"]
        cost       = round(price * COGS_RATE, 4)
        profit     = round(price - cost, 4)
        waste_loss = round(cost * WASTE_PENALTY, 4)
        donuts.append({
            "name": name, "price": price, "cost": cost,
            "profit": profit, "waste_loss": waste_loss, "demand": demand,
        })

    model  = cp_model.CpModel()
    solver = cp_model.CpSolver()

    q = []
    for d in donuts:
        ub = max(int(d["demand"]), 0)
        q.append(model.NewIntVar(0, ub, f"q_{d['name'].replace(' ', '_')}"))

    budget_scaled = int(budget * SCALE)
    cost_terms = [math.ceil(d["cost"] * SCALE) * q[i] for i, d in enumerate(donuts)]
    model.Add(sum(cost_terms) <= budget_scaled)

    profit_terms = [int(d["profit"] * SCALE) * q[i] for i, d in enumerate(donuts)]
    model.Maximize(sum(profit_terms))

    solver.parameters.max_time_in_seconds = 10.0
    status = solver.Solve(model)

    status_map = {
        cp_model.OPTIMAL:    "OPTIMAL",
        cp_model.FEASIBLE:   "FEASIBLE",
        cp_model.INFEASIBLE: "INFEASIBLE",
        cp_model.UNKNOWN:    "UNKNOWN",
    }
    status_str = status_map.get(status, "UNKNOWN")

    donut_plan        = {}
    total_revenue     = 0.0
    total_cost        = 0.0
    total_profit      = 0.0
    total_waste_units = 0
    total_waste_value = 0.0

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        for i, d in enumerate(donuts):
            qty_produced = solver.Value(q[i])
            revenue      = round(qty_produced * d["price"], 2)
            prod_cost    = round(qty_produced * d["cost"],  2)
            profit       = round(revenue - prod_cost,       2)

            donut_plan[d["name"]] = {
                "qty_to_produce":   qty_produced,
                "predicted_demand": round(d["demand"], 2),
                "unit_price":       round(d["price"],  2),
                "unit_cost":        round(d["cost"],   2),
                "revenue":          revenue,
                "production_cost":  prod_cost,
                "profit":           profit,
                "waste_units":      0,
                "waste_value":      0.0,
            }
            total_revenue += revenue
            total_cost    += prod_cost
            total_profit  += profit
    else:
        for d in donuts:
            donut_plan[d["name"]] = {
                "qty_to_produce": 0, "predicted_demand": round(d["demand"], 2),
                "unit_price": round(d["price"], 2), "unit_cost": round(d["cost"], 2),
                "revenue": 0, "production_cost": 0,
                "profit": 0, "waste_units": 0, "waste_value": 0,
            }

    drink_plan    = {}
    drink_revenue = 0.0
    for name, info in drink_data.items():
        rev = round(info["predicted_demand"] * info["unit_price"], 2)
        drink_plan[name] = {
            "predicted_demand":  round(info["predicted_demand"], 2),
            "unit_price":        round(info["unit_price"],       2),
            "estimated_revenue": rev,
        }
        drink_revenue += rev

    total_revenue = round(total_revenue + drink_revenue, 2)
    total_profit  = round(total_profit  + drink_revenue, 2)
    total_cost    = round(total_cost, 2)

    return {
        "status":     status_str,
        "inputs":     {"budget": budget, **user_inputs},
        "donut_plan": donut_plan,
        "drink_plan": drink_plan,
        "summary": {
            "total_revenue":         total_revenue,
            "total_production_cost": total_cost,
            "total_profit":          total_profit,
            "total_waste_units":     total_waste_units,
            "total_waste_value":     total_waste_value,
            "budget_used":           total_cost,
            "budget_remaining":      round(budget - total_cost, 2),
        },
    }


def main():
    import sys
    import pandas as pd
    sys.path.insert(0, ".")
    from demand import calculate_demand

    sales = pd.read_csv("bakery_sales.csv")

    budget      = input("Budget ($): ")
    location    = input("Location (e.g. New York): ")
    time_of_day = input("Time of Day (Morning / Afternoon / Evening): ")
    promotion   = input("Promotion (Yes / No): ")

    demand_out = calculate_demand([budget, time_of_day, promotion, location], sales)
    result     = optimize_production(demand_out)

    print(f"\nStatus : {result['status']}")
    for name, v in result["donut_plan"].items():
        print(f"  {name:22s}  produce={v['qty_to_produce']:4d}  profit=${v['profit']:7.2f}")
    print()
    for k, v in result["summary"].items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
