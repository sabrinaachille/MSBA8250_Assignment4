import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

sales = pd.read_csv("bakery_sales.csv")

def build_model(sales, item_col, quantity_col, price_col):
    features = [item_col, price_col, "promotion", "time_of_day", "location"]
    target = quantity_col

    df = sales.dropna(subset=features + [target])

    X = df[features]
    y = df[target]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), [item_col, "promotion", "time_of_day", "location"]),
            ("num", "passthrough", [price_col])
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
        ]
    )

    model.fit(X, y)

    return model


def calculate_demand(user_input, sales):
    """
    user_input format:
    [budget, time_of_day, promotion, location]
    """
    
    budget = float(user_input[0])
    time_of_day = user_input[1]
    promotion = user_input[2]
    location = user_input[3]

    donut_model = build_model(
        sales,
        item_col="donut_item",
        quantity_col="donut_units_sold",
        price_col="donut_unit_price"
    )

    drink_model = build_model(
        sales,
        item_col="drink_item",
        quantity_col="drink_units_sold",
        price_col="drink_unit_price"
    )

    donut_predictions = {}
    drink_predictions = {}

    for donut in sales["donut_item"].dropna().unique():
        avg_price = sales.loc[sales["donut_item"] == donut, "donut_unit_price"].mean()

        input_data = pd.DataFrame({
            "donut_item": [donut],
            "donut_unit_price": [avg_price],
            "promotion": [promotion],
            "time_of_day": [time_of_day],
            "location": [location]
        })

        predicted_demand = donut_model.predict(input_data)[0]

        donut_predictions[donut] = {
            "predicted_demand": round(max(predicted_demand, 0), 2),
            "unit_price": round(avg_price, 2),
            "estimated_sales": round(max(predicted_demand, 0) * avg_price, 2)
        }

    for drink in sales["drink_item"].dropna().unique():
        avg_price = sales.loc[sales["drink_item"] == drink, "drink_unit_price"].mean()

        input_data = pd.DataFrame({
            "drink_item": [drink],
            "drink_unit_price": [avg_price],
            "promotion": [promotion],
            "time_of_day": [time_of_day],
            "location": [location]
        })

        predicted_demand = drink_model.predict(input_data)[0]

        drink_predictions[drink] = {
            "predicted_demand": round(max(predicted_demand, 0), 2),
            "unit_price": round(avg_price, 2),
            "estimated_sales": round(max(predicted_demand, 0) * avg_price, 2)
        }

    return {
        "budget": budget,
        "inputs": {
            "time_of_day": time_of_day,
            "promotion": promotion,
            "location": location
        },
        "donut_demand": donut_predictions,
        "drink_demand": drink_predictions
    }


def validate_single_model(sales, item_col, quantity_col, price_col):
    features = [item_col, price_col, "promotion", "time_of_day", "location"]
    target = quantity_col

    df = sales.dropna(subset=features + [target])

    X = df[features]
    y = df[target]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), [item_col, "promotion", "time_of_day", "location"]),
            ("num", "passthrough", [price_col])
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    return {
        "r_squared": round(r2, 4),
        "mse": round(mse, 4),
        "rmse": round(rmse, 4),
        "mae": round(mae, 4)
    }


def validate_demand(user_input, sales):
    donut_validation = validate_single_model(
        sales,
        item_col="donut_item",
        quantity_col="donut_units_sold",
        price_col="donut_unit_price"
    )

    drink_validation = validate_single_model(
        sales,
        item_col="drink_item",
        quantity_col="drink_units_sold",
        price_col="drink_unit_price"
    )

    return {
        "donut_model_validation": donut_validation,
        "drink_model_validation": drink_validation
    }


def main():
    budget = input("Budget: ")
    time_of_day = input("Time of day: ")
    promotion = input("Promotion Yes/No: ")
    location = input("Location: ")

    user_input = [budget, time_of_day, promotion, location]

    demand = calculate_demand(user_input, sales)
    validation = validate_demand(user_input, sales)

    print("\nPredicted demand:")
    print(demand)

    print("\nValidation results:")
    print(validation)


if __name__ == "__main__":
    main()