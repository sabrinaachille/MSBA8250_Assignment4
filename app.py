from shiny import App, ui, render, reactive
from demand import calculate_demand, sales
from optimizer import optimize_production
import pandas as pd
import plotly.express as px

app_ui = ui.page_navbar(

    # ------------- Dashboard Tab ---------------------------
    ui.nav_panel(
        "Dashboard",

        ui.card(
            ui.card_header("KPI"),

            ui.div(
                {"class": "kpi-row"},

                ui.div(
                    {"class": "kpi-group"},
                    ui.p("Total Sales"),
                    ui.h3("$---")
                ),

                ui.div(
                    {"class": "kpi-group"},
                    ui.p("Total Units Sold"),
                    ui.h3("----")
                ),

                ui.div(
                    {"class": "kpi-group"},
                    ui.p("Average Rating"),
                    ui.h3("----")
                ),

                ui.div(
                    {"class": "kpi-group"},
                    ui.p("Waste %"),
                    ui.h3("----")
                ),
            ),
        ),

        ui.br(),

        ui.p("Visualization content here"),

        ui.br(),

        ui.layout_columns(
            ui.card(
                ui.card_header("Sales Trend"),
                ui.output_ui("sales_trend_chart")
            ),
            ui.card(
                ui.card_header("Top Products"),
                ui.output_ui("top_products_chart")
            ),
            col_widths=[6, 6]
        ),

        ui.br(),

        ui.card(
            ui.card_header("Sales by Time of Day"),
            ui.output_ui("sales_by_time_chart")
        ),
    ),
    # ------------- Planner Tab ------------------------------
    ui.nav_panel(
        "Planner",

        # ------------------------ Input Card ----------------
        ui.card(
            ui.card_header("Input"),

            ui.div(
                {"class": "input-row"},

                ui.div(
                    {"class": "input-group"},
                    ui.input_numeric("budget", "Budget", value=500),
                ),

                ui.div(
                    {"class": "input-group"},
                    ui.input_select(
                        "location",
                        "Location",
                        ["New York", "Boston", "Chicago", "Miami", "Los Angeles"]
                    ),
                ),

                ui.div(
                    {"class": "input-group"},
                    ui.input_select(
                        "time_of_day",
                        "Time of Day",
                        ["Morning", "Afternoon", "Evening"]
                    ),
                ),

                ui.div(
                    {"class": "input-group promotion-group"},
                    ui.tags.label("Promotion"),
                    ui.input_checkbox("promo", "", value=False),
                ),
            ),
        ),

        ui.br(),

        # ------------------------ Demand Output Card ----------------
        ui.card(
            ui.card_header(
                ui.div(
                    {"class": "card-header-flex"},
                    ui.h5("Expected Demand"),
                    ui.input_action_button(
                        "predict",
                        "Run Prediction",
                        class_="header-button"
                    )
                )
            ),
            ui.output_ui("demand_output")
        ),

        ui.br(),

        # ------------------------ Optimization Output Card ----------------
        ui.card(
            ui.card_header(
                ui.div(
                    {"class": "card-header-flex"},
                    ui.h5("Recommended Plan"),
                    ui.input_action_button(
                        "optimize",
                        "Run Optimization",
                        class_="header-button"
                    )
                )
            ),
            ui.output_ui("optimization_output"),
        )
    ),

    title="SVNG Demo",
    id="page",
    header=ui.include_css("www/style.css")
)


def server(input, output, session):

    # ── Dashboard Data Prep ───────────────────────────────────────────────────
    def dashboard_data():
        df = sales.copy()
        df["date"] = pd.to_datetime(df["date"])
        return df


    # ── Visualization 1: Sales Trend Line Chart ───────────────────────────────
    @output
    @render.ui
    def sales_trend_chart():
        df = dashboard_data()

        sales_by_date = (
            df.groupby("date", as_index=False)["total_sales"]
            .sum()
            .sort_values("date")
        )

        sales_by_date["7_day_avg"] = (
            sales_by_date["total_sales"]
            .rolling(window=7, min_periods=1)
            .mean()
        )

        fig = px.line(
            sales_by_date,
            x="date",
            y=["total_sales", "7_day_avg"],
            title="Total Sales Trend with 7-Day Average",
            markers=True,
            labels={
                "date": "Date",
                "value": "Sales",
                "variable": "Metric"
            }
        )

        fig.update_layout(
            margin=dict(l=20, r=20, t=50, b=20),
            legend_title_text=""
        )

        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs="cdn"))


    # ── Visualization 2: Top Products Bar Chart ───────────────────────────────
    @output
    @render.ui
    def top_products_chart():
        df = dashboard_data()

        top_products = (
            df.groupby("donut_item", as_index=False)["donut_units_sold"]
            .sum()
            .sort_values("donut_units_sold", ascending=False)
            .head(10)
        )

        fig = px.bar(
            top_products,
            x="donut_item",
            y="donut_units_sold",
            title="Top Donut Products by Units Sold",
            labels={
                "donut_item": "Donut Product",
                "donut_units_sold": "Units Sold"
            }
        )

        fig.update_layout(
            margin=dict(l=20, r=20, t=50, b=80),
            xaxis_tickangle=-35
        )

        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs="cdn"))


    # ── Visualization 3: Sales by Time of Day Bar Chart ───────────────────────
    @output
    @render.ui
    def sales_by_time_chart():
        df = dashboard_data()

        time_order = ["Morning", "Afternoon", "Evening"]

        sales_by_time = (
            df.groupby("time_of_day", as_index=False)["total_sales"]
            .sum()
        )

        sales_by_time["time_of_day"] = pd.Categorical(
            sales_by_time["time_of_day"],
            categories=time_order,
            ordered=True
        )

        sales_by_time = sales_by_time.sort_values("time_of_day")

        fig = px.bar(
            sales_by_time,
            x="time_of_day",
            y="total_sales",
            title="Sales by Time of Day",
            labels={
                "time_of_day": "Time of Day",
                "total_sales": "Total Sales"
            }
        )

        fig.update_layout(
            margin=dict(l=20, r=20, t=50, b=20)
        )

        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs="cdn"))

   # ── Expected Demand ───────────────────────────────────────────────────────
    @output
    @render.ui
    @reactive.event(input.predict)
    def demand_output():

        promo_value = "Yes" if input.promo() else "No"

        user_input = [
            input.budget(),
            input.time_of_day(),
            promo_value,
            input.location()
        ]

        results = calculate_demand(user_input, sales)

        donut_rows = [
            ui.tags.tr(
                ui.tags.td(item),
                ui.tags.td(values["predicted_demand"]),
                ui.tags.td(f"${values['estimated_sales']}")
            )
            for item, values in results["donut_demand"].items()
        ]

        drink_rows = [
            ui.tags.tr(
                ui.tags.td(item),
                ui.tags.td(values["predicted_demand"]),
                ui.tags.td(f"${values['estimated_sales']}")
            )
            for item, values in results["drink_demand"].items()
        ]

        return ui.div(
            ui.h5("Donuts"),
            ui.tags.table(
                {"class": "demand-table"},
                ui.tags.thead(
                    ui.tags.tr(
                        ui.tags.th("Item"),
                        ui.tags.th("Units"),
                        ui.tags.th("Estimated Sale")
                    )
                ),
                ui.tags.tbody(*donut_rows)
            ),

            ui.br(),

            ui.h5("Drinks"),
            ui.tags.table(
                {"class": "demand-table"},
                ui.tags.thead(
                    ui.tags.tr(
                        ui.tags.th("Item"),
                        ui.tags.th("Units"),
                        ui.tags.th("Estimated Sale")
                    )
                ),
                ui.tags.tbody(*drink_rows)
            )
        )

    # ── Recommended Plan ──────────────────────────────────────────────────────
    @output
    @render.ui
    @reactive.event(input.optimize)
    def optimization_output():

        promo_value = "Yes" if input.promo() else "No"

        user_input = [
            input.budget(),
            input.time_of_day(),
            promo_value,
            input.location()
        ]

        demand_out = calculate_demand(user_input, sales)
        result     = optimize_production(demand_out)
        s          = result["summary"]

        # Infeasible guard
        if result["status"] not in ("OPTIMAL", "FEASIBLE"):
            return ui.div(
                ui.p(
                    "No feasible plan found. Try increasing your budget.",
                    style="color:red; padding:12px 0;"
                )
            )

        # Summary metrics row
        summary_row = ui.div(
            {"style": "display:flex; gap:24px; flex-wrap:wrap; margin-bottom:20px;"},
            ui.div(
                ui.p("Total Profit",     style="margin:0; font-size:0.75rem; color:#888; text-transform:uppercase; letter-spacing:1px;"),
                ui.h4(f"${float(s['total_profit']):.2f}",     style="margin:4px 0 0;"),
            ),
            ui.div(
                ui.p("Total Revenue",    style="margin:0; font-size:0.75rem; color:#888; text-transform:uppercase; letter-spacing:1px;"),
                ui.h4(f"${float(s['total_revenue']):.2f}",    style="margin:4px 0 0;"),
            ),
            ui.div(
                ui.p("Budget Used",      style="margin:0; font-size:0.75rem; color:#888; text-transform:uppercase; letter-spacing:1px;"),
                ui.h4(f"${float(s['budget_used']):.2f}",      style="margin:4px 0 0;"),
            ),
            ui.div(
                ui.p("Budget Remaining", style="margin:0; font-size:0.75rem; color:#888; text-transform:uppercase; letter-spacing:1px;"),
                ui.h4(f"${float(s['budget_remaining']):.2f}", style="margin:4px 0 0;"),
            ),
        )

        # Donut table
        th_style = "text-align:left; padding:8px 10px; border-bottom:2px solid #dee2e6; font-size:0.75rem; text-transform:uppercase; color:#888;"
        td_style = "padding:8px 10px; border-bottom:1px solid #f0f0f0;"

        donut_rows = [
            ui.tags.tr(
                ui.tags.td(name,                           style=td_style),
                ui.tags.td(str(v["qty_to_produce"]),       style=td_style),
                ui.tags.td(f"{v['predicted_demand']:.1f}", style=td_style),
                ui.tags.td(f"${v['unit_price']:.2f}",      style=td_style),
                ui.tags.td(f"${v['production_cost']:.2f}", style=td_style),
                ui.tags.td(f"${v['profit']:.2f}",          style=td_style),
            )
            for name, v in result["donut_plan"].items()
        ]

        donut_table = ui.div(
            ui.h5("Donuts", style="margin-bottom:10px;"),
            ui.tags.table(
                {"style": "width:100%; border-collapse:collapse; font-size:0.875rem;"},
                ui.tags.thead(
                    ui.tags.tr(*[
                        ui.tags.th(col, style=th_style)
                        for col in ["Item", "Qty to Produce", "Predicted Demand", "Unit Price", "Production Cost", "Profit"]
                    ])
                ),
                ui.tags.tbody(*donut_rows),
            )
        )

        # Drink table
        drink_rows = [
            ui.tags.tr(
                ui.tags.td(name,                              style=td_style),
                ui.tags.td(f"{v['predicted_demand']:.1f}",   style=td_style),
                ui.tags.td(f"${v['unit_price']:.2f}",        style=td_style),
                ui.tags.td(f"${v['estimated_revenue']:.2f}", style=td_style),
            )
            for name, v in result["drink_plan"].items()
        ]

        drink_table = ui.div(
            ui.h5("Drinks", style="margin-top:24px; margin-bottom:10px;"),
            ui.tags.table(
                {"style": "width:100%; border-collapse:collapse; font-size:0.875rem;"},
                ui.tags.thead(
                    ui.tags.tr(*[
                        ui.tags.th(col, style=th_style)
                        for col in ["Item", "Expected Demand", "Unit Price", "Est. Revenue"]
                    ])
                ),
                ui.tags.tbody(*drink_rows),
            )
        )

        return ui.div(
            summary_row,
            donut_table,
            drink_table,
        )


app = App(app_ui, server)     
