from shiny import App, ui

app_ui = ui.page_navbar(  
    #Dashboard Tab
    ui.nav_panel(
        "Dashboard", 
        "Visualization content"),  
    
    #Planner Tab
    ui.nav_panel(
        "Planner",
        ui.layout_columns(
            
            #Input Card
            ui.card(
                ui.card_header("Inputs"),
                
                #Budget Row
                ui.layout_columns(
                    ui.markdown("**Budget**"),
                    ui.input_numeric(
                        "budget", 
                        None, 
                        500
                    ),
                    col_widths=(5,7)
                ),

                #Day of Week Row
                ui.layout_columns(
                    ui.markdown("**Day of Week**"),
                    ui.input_select(
                        "day",
                        None,
                        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                    ),
                    col_widths=(5,7)
                ),

                #Weather Row
                ui.layout_columns(
                    ui.markdown("**Weather (F)**"),
                    ui.input_numeric(
                        "weather",
                        None,
                        70
                    ),
                    col_widths=(5,7)
                ),

                #Promotion Row
                ui.layout_columns(
                    ui.markdown("**Promotion**"),
                    ui.input_checkbox(
                        "promo",
                        None,
                        False
                    ),
                    col_widths=(5,7)
                ),

                ui.br(),
                
                #Button
                ui.input_action_button(
                    "predict", 
                    "Run Prediction", 
                    width="100%"
                ),
            ),

            #Output Card
            ui.card(
                ui.card_header("Results"),
                "Predictive and Optimization ouput here",
                ui.br(),
                ui.input_action_button(
                    "optimize", 
                    "Run Optimization"
                ),
            ),
            
            col_widths=(5, 7),
        )
    ),
    title="SVNG Demo",  
    id="page",  
)  

def server(input, output, session):
    pass

app = App(app_ui, server)