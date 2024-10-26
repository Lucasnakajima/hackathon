import pandas as pd
import re
import math

# Constants provided for the challenge
ORDER_COST = 10.0
HOLDING_COST = 0.7
LEAD_TIME = 7  # in days
SAFETY_STOCK = 1000
ANNUAL_DEMAND = 50000
MATERIAL_PRICES = {
    "tecido": 7.0,
    "algodao": 5.5,
    "fio": 4.5,
    "poliester": 10.0
}

# Size ratio multiplier
SIZE_RATIO = {
    "XS": 0.5,
    "S": 0.75,
    "M": 1.0,
    "L": 1.5,
    "XL": 2.0
}

# 150 CALCOES XS

# Base material requirements per clothing type
MATERIALS_BASE = {
    "Tshirt": {"tecido": 1.0, "algodao": 0.8, "fio": 0.4, "poliester": 1.3},
    "Calcoes": {"tecido": 0.8, "algodao": 0.7, "fio": 0.4, "poliester": 1.4},
    "Camisola": {"tecido": 0.5, "algodao": 0.35, "fio": 0.5, "poliester": 1.15},
    "Calcas": {"tecido": 1.2, "algodao": 0.95, "fio": 0.35, "poliester": 1.5}
}

# Function to calculate the Economic Order Quantity (EOQ)
def calculate_economic_order_quantity():
    return math.sqrt((2 * ANNUAL_DEMAND * ORDER_COST) / HOLDING_COST)

# Function to calculate the reorder point
def calculate_reorder_point(daily_demand):
    return (daily_demand * LEAD_TIME) + SAFETY_STOCK

# Function to read orders from different file formats and load them into a DataFrame
def read_orders_to_dataframe(file_path):
    orders = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            # Format 1: Quantity Type Size (e.g., "135 Sweater XL")
            if re.match(r'^\d+\s+\w+\s+\w+$', line):
                quantity, clothing_type, size = line.split()
                
                orders.append({
                                "Quantity": int(quantity),
                                "Type": clothing_type,
                                "Size": size.upper()
                            })
                
            # Format 2: QuantityTypeSize combined (e.g., "145SweaterXL")
            elif re.match(r'^\d+\w+\w+$', line):
                matches = re.findall(r'(\d+[A-Z][a-z]+[A-Z]+)', line)
                if matches:
                    for match in matches:
                        order = re.match(r'(\d+)([A-Z][a-z]+)([A-Z]+)', match)
                        if order:
                            quantity = order.group(1)
                            clothing_type = order.group(2)
                            size = order.group(3)
                            
                            orders.append({
                                "Quantity": int(quantity),
                                "Type": clothing_type,
                                "Size": size.upper()
                            })
                        else:
                            continue  # Skip lines that do not match any known format
                        
            # Format 3: Quantity Type "do tamanho" Size (e.g., "145 Sweater do tamanho L")
            else:
                matches = re.findall(r'(\d+)\s+(\w+)\s+do tamanho\s+(\w+)', line)
                if matches:
                    for order in matches:
                        quantity = order[0]
                        clothing_type = order[1]
                        size = order[2]
                        
                        orders.append({
                            "Quantity": int(quantity),
                            "Type": clothing_type,
                            "Size": size.upper()
                        })
    
    return orders

# Function to calculate required materials for each order
def calculate_materials_needed(order):
    clothing_type = order["Type"]
    size = order["Size"]
    quantity = order["Quantity"]
    
    size_multiplier = SIZE_RATIO.get(size, 1)
    materials_needed = {}
    
    # Calculate material requirement based on base quantity and size multiplier
    # INTEGRAR BASE DE DADOS
    for material, base_amount in MATERIALS_BASE[clothing_type].items():
        materials_needed[material] = quantity * base_amount * size_multiplier
    
    return materials_needed

# Function to calculate total cost for materials in an order
def calculate_order_cost(materials):
    total_cost = 0.0
    for material, amount in materials.items():
        material_price = MATERIAL_PRICES.get(material, 0)
        total_cost += amount * material_price
    return total_cost

# Example main function to process orders from file and calculate materials and costs
def main():
    daily_demand = ANNUAL_DEMAND / 365
    eoq = calculate_economic_order_quantity()
    reorder_point = calculate_reorder_point(daily_demand)
    
    print(f"Economic Order Quantity (EOQ): {eoq}")
    print(f"Reorder Point: {reorder_point}")
    
    # Process each file and display orders with materials and cost
    all_data = []
    for file_name in ['./encomenda1.txt', './encomenda2.txt', './encomenda3.txt']:
        print(f"\nProcessing file: {file_name}")
        orders_df = read_orders_to_dataframe(file_name)
        all_data.extend(orders_df)
    
    df = pd.DataFrame(all_data)
    print(df)
    df.to_excel('output.xlsx', index=False)
        
    for _, order in df.iterrows():
        materials = calculate_materials_needed(order)
        cost = calculate_order_cost(materials)
        # print(f"Order: {order.to_dict()}")
        # print(f"Materials Needed: {materials}")
        # print(f"Total Cost: €{cost:.2f}")
        # print("------")

if __name__ == "__main__":
    main()
