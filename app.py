from shiny import App, ui, render, reactive
from demand import calculate_demand, sales


app_ui = ui.page_navbar(

    # ------------- Dashboard Tab ---------------------------
    ui.nav_panel(
        "Dashboard",

        ui.card(
            ui.card_header("KPI"),

            ui.div(
                {"class": "kpi-row"},

                # Budget Input
                ui.div(
                    {"class": "kpi-group"},
                    ui.p("Total Sales"),
                    ui.h3("$---")
                ),

                # Location Input
                ui.div(
                    {"class": "kpi-group"},
                    ui.p("Total Units Sold"),
                    ui.h3("----")
                ),

                # Time of Day Input
                ui.div(
                    {"class": "kpi-group"},
                    ui.p("Average Rating"),
                    ui.h3("----")
                ),

                # Promotion Input
                ui.div(
                    {"class": "kpi-group"},
                    ui.p("Waste %"),
                    ui.h3("----")
                ),
            ),
        ),

        ui.br(),

        ui.p("Visualization content here")
    ),

    # ------------- Planner Tab ------------------------------
    ui.nav_panel(
        "Planner",

        # ------------------------ Input Card ----------------
        ui.card(
            ui.card_header("Input"),

            ui.div(
                {"class": "input-row"},

                # Budget Input
                ui.div(
                    {"class": "input-group"},
                    ui.input_numeric("budget", "Budget", value=500),
                ),

                # Location Input
                ui.div(
                    {"class": "input-group"},
                    ui.input_select(
                        "location",
                        "Location",
                        ["New York", "Boston", "Chicago", "Miami", "Los Angeles"]
                    ),
                ),

                # Time of Day Input
                ui.div(
                    {"class": "input-group"},
                    ui.input_select(
                        "time_of_day",
                        "Time of Day",
                        ["Morning", "Afternoon", "Evening"]
                    ),
                ),

                # Promotion Input
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

        # --- Format Donut Output ---
        donut_list = [
            ui.tags.li(
                f"{item}: {values['predicted_demand']} units "
                f"(Estimated Sales: ${values['estimated_sales']})"
            )
            for item, values in results["donut_demand"].items()
        ]

        # --- Format Drink Output ---
        drink_list = [
            ui.tags.li(
                f"{item}: {values['predicted_demand']} units "
                f"(Estimated Sales: ${values['estimated_sales']})"
            )
            for item, values in results["drink_demand"].items()
        ]

        return ui.div(
            ui.h5("Donuts"),
            ui.tags.ul(*donut_list),

            ui.h5("Drinks"),
            ui.tags.ul(*drink_list)
        )

    @output
    @render.ui
    @reactive.event(input.optimize)
    def optimization_output():
        return ui.div(
            ui.p("Optimization recommendation will display here.")
        )


app = App(app_ui, server)