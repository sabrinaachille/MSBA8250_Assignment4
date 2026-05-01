import pandas as pd

sales = pd.read_csv('bakery_sales.csv')

def calculate_demand(user_input, sales):
    # Placeholder for demand calculation logic
    # This is where you would implement your demand forecasting model
    return "Predicted demand based on user input: " + str(user_input)

def validate_demand(user_input, sales):
    # Placeholder for demand validation logic
    # This is where you would implement your demand validation logic
    return "Validated demand based on user input: " + str(user_input)

def main():
    user_input = input("Budget: ")
    demand = calculate_demand(user_input, sales)
    validation = validate_demand(user_input, sales)
    print("Predicted demand: ", demand, "\n","Validated demand: ", validation)

print(sales['Dnt_item_name'].unique())
print(sales['Drink_Item'].unique())