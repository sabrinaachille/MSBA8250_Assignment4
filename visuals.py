import pandas as pd
import plotly.express as px


def prepare_dashboard_data(sales):
    df = sales.copy()
    df["date"] = pd.to_datetime(df["date"])
    return df


def get_total_sales(sales):
    df = prepare_dashboard_data(sales)
    total_sales = df["total_sales"].sum()
    return f"${total_sales:,.2f}"


def get_total_units_sold(sales):
    df = prepare_dashboard_data(sales)
    total_units = df["donut_units_sold"].sum() + df["drink_units_sold"].sum()
    return f"{int(total_units):,}"


def get_average_rating(sales):
    df = prepare_dashboard_data(sales)
    avg_rating = df["customer_rating"].mean()
    return f"{avg_rating:.2f}"


def get_waste_percent(sales):
    df = prepare_dashboard_data(sales)

    total_made = df["donut_units_made"].sum()
    total_waste = df["donut_waste"].sum()

    if total_made == 0:
        return "0.0%"

    waste_percent = total_waste / total_made
    return f"{waste_percent:.1%}"


def create_sales_trend_chart(sales):
    df = prepare_dashboard_data(sales)

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

    return fig


def create_top_products_chart(sales):
    df = prepare_dashboard_data(sales)

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

    return fig


def create_sales_by_time_chart(sales):
    df = prepare_dashboard_data(sales)

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

    return fig
