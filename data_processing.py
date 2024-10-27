import pandas as pd
import re
import math

# Constants provided for the challenge
ORDER_COST = 10.0
HOLDING_COST = 0.7
LEAD_TIME = 7  # in days
SAFETY_STOCK = 1000
INITIAL_STOCK = 2200
ANNUAL_DEMAND = 50000
MATERIAL_PRICES = {
    "tecido": 7.0,
    "algodao": 5.5,
    "fio": 4.5,
    "poliester": 10.0
}

# Size ratio multiplier and base requirements per type
SIZE_RATIO = {"XS": 0.5, "S": 0.75, "M": 1.0, "L": 1.5, "XL": 2.0}
MATERIALS_BASE = {
    "Tshirt": {"tecido": 1.0, "algodao": 0.8, "fio": 0.4, "poliester": 1},
    "Calcoes": {"tecido": 0.8, "algodao": 0.7, "fio": 0.4, "poliester": 0.8},
    "Camisola": {"tecido": 0.5, "algodao": 0.35, "fio": 0.5, "poliester": 0.5},
    "Calcas": {"tecido": 1.2, "algodao": 0.95, "fio": 0.35, "poliester": 1.2}
}

# Function to calculate EOQ and reorder point
def calculate_economic_order_quantity():
    return math.sqrt((2 * ANNUAL_DEMAND * ORDER_COST) / HOLDING_COST)

def calculate_reorder_point():
    return ((ANNUAL_DEMAND / 365) * LEAD_TIME) + SAFETY_STOCK

# Function to accumulate material quantities for an order
def calculate_materials_needed(order):
    materials_needed = {}
    size_multiplier = SIZE_RATIO.get(order["Size"], 1)
    for material, base_amount in MATERIALS_BASE[order["Type"]].items():
        materials_needed[material] = materials_needed.get(material, 0) + order["Quantity"] * base_amount * size_multiplier
    return materials_needed


def request_materials(eoq, orders, material):
    # orders[material] -= eoq
    print(f"EOQ: {eoq}")
    # Send PDF
    return {material: eoq}


def check_reorder_point(orders, stock, day, reorder_point, pending_orders):
    # Inicialize o acumulador de materiais para o dia
    materials_acc = {"tecido": 0, "algodao": 0, "fio": 0, "poliester": 0}
    
    # Acumular materiais necessários para os pedidos do dia
    for order in orders:
        required_materials = calculate_materials_needed(order)
        for material, amount in required_materials.items():
            materials_acc[material] += amount
    
    print(f"Day {day}: Material accumulation for the day: {materials_acc}")

    # Verificar se há entregas pendentes para o dia e atualizar o estoque
    if day in pending_orders:
        for material, amount in pending_orders.pop(day).items():
            stock[material] += amount
            print(f"Delivered {amount} of {material} to stock on day {day}. Current stock after delivery: {stock[material]}")

    
    # Verificar se o ponto de encomenda foi atingido para cada material
    for material, required in materials_acc.items():
        
        # Calcular estoque efetivo após considerar a demanda do dia
        effective_stock = stock[material] - required
        
        # Verificar necessidade de reorder apenas se o estoque efetivo está abaixo do ponto de encomenda
        if effective_stock <= reorder_point:
            eoq = calculate_economic_order_quantity()
            delivery_day = day + LEAD_TIME
            
            # Encomendar apenas se não houver encomenda já pendente para esse material
            if delivery_day not in pending_orders:
                pending_orders[delivery_day] = {}
            if material not in pending_orders[delivery_day]:
                pending_orders[delivery_day][material] = eoq
                print(f"Order placed for {eoq} units of {material}, arriving on day {delivery_day}")

    # Atualizar o estoque subtraindo a quantidade necessária para o dia
    today_materials = calculate_materials_needed(orders[-1])
    for material, amount in today_materials.items():
        today_materials[material] += amount
            
    for material, used in today_materials.items():
        stock[material] -= used  # subtrai apenas o necessário para o dia
        print(f"Stock of {material} after using {used} units for day {day}: {stock[material]}")
    
    return stock


# Main function to process each order file and track stock
def main():
    reorder_point = calculate_reorder_point()
    
    stock = {
        "tecido": INITIAL_STOCK,
        "algodao": INITIAL_STOCK,
        "fio": INITIAL_STOCK,
        "poliester": INITIAL_STOCK
    }  # Initial stock
    
    pending_orders = {}  # Pending orders by day
    
    day = 0
    for file_name in ['./encomenda1.txt', './encomenda2.txt', './encomenda3.txt']:
        with open(file_name, 'r') as file:
            orders = []
            for line in file:
                line = line.strip()
                day += 1

                # Format handling (process each order line based on the specified format)
                if re.match(r'^\d+\s+\w+\s+\w+$', line):
                    quantity, clothing_type, size = line.split()
                    orders.append({"Quantity": int(quantity), "Type": clothing_type, "Size": size.upper()})
                elif re.match(r'^\d+\w+\w+$', line):
                    matches = re.findall(r'(\d+[A-Z][a-z]+[A-Z]+)', line)
                    for match in matches:
                        order = re.match(r'(\d+)([A-Z][a-z]+)([A-Z]+)', match)
                        if order:
                            orders.append({"Quantity": int(order.group(1)), "Type": order.group(2), "Size": order.group(3).upper()})
                else:
                    matches = re.findall(r'(\d+)\s+(\w+)\s+do tamanho\s+(\w+)', line)
                    for match in matches:
                        orders.append({"Quantity": int(match[0]), "Type": match[1], "Size": match[2].upper()})
                
                # Check reorder point and update stock
                stock = check_reorder_point(orders, stock, day, reorder_point, pending_orders)

    # Output final stock levels
    print("Final stock levels:", stock)

if __name__ == "__main__":
    main()
