from fpdf import FPDF
from datetime import datetime
import pandas as pd
import re
import math

# Constantes e funções originais (como MATERIAL_PRICES, SIZE_RATIO, etc.) mantidos aqui...
MATERIAL_PRICES = {
    "fabric": 7.0,
    "cotton": 5.5,
    "thread": 4.5,
    "polyester": 10.0
}

AGGREGATED_MATERIALS = {
    'polyester': 100,  # 100 units of polyester
    'thread': 200,     # 200 units of thread
    'cotton': 150,     # 150 units of cotton
    'fabric': 80       # 80 units of fabric
}
TOTAL_COST = 500
# Função para gerar a nota de encomenda em formato PDF
def generate_supplier_order_pdf(aggregated_materials, total_cost):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    
    # Informações do cabeçalho
    pdf.cell(0, 10, "Nota de Encomenda SciTeCh'24", ln=True, align='C')
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, f"Data: {datetime.now().strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(0, 10, f"Encomenda Nº: 197456", ln=True)
    
    # Informações da empresa fornecedora
    pdf.ln(10)
    pdf.cell(0, 10, "Fornecedor:", ln=True)
    pdf.cell(0, 10, "SciTeCh Textile Engineering", ln=True)
    pdf.cell(0, 10, "Avenida dos Tecidos Nº42", ln=True)
    pdf.cell(0, 10, "Espaço Industrial Marciano", ln=True)
    
    # Tabela de materiais encomendados
    pdf.ln(10)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(40, 10, "Artigo", border=1)
    pdf.cell(30, 10, "Quantidade", border=1, align='C')
    pdf.cell(30, 10, "Preço Unitário", border=1, align='C')
    pdf.cell(30, 10, "Subtotal", border=1, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 10)
    for material, amount in aggregated_materials.items():
        unit_price = MATERIAL_PRICES.get(material, 0)
        subtotal = amount * unit_price
        pdf.cell(40, 10, material.capitalize(), border=1)
        pdf.cell(30, 10, f"{amount:.0f} unidades", border=1, align='C')
        pdf.cell(30, 10, f"€{unit_price:.2f}", border=1, align='C')
        pdf.cell(30, 10, f"€{subtotal:.2f}", border=1, align='C')
        pdf.ln(10)
    
    # Total
    pdf.set_font("Arial", "B", 10)
    pdf.cell(100, 10, "Total:", border=1)
    pdf.cell(30, 10, f"€{total_cost:.2f}", border=1, align='C')
    
    # Informações adicionais e rodapé
    pdf.ln(20)
    pdf.set_font("Arial", "", 8)
    pdf.cell(0, 10, "Método de Pagamento: Transferência Bancária", ln=True)
    pdf.cell(0, 10, "Termos e Condições: Sujeito a confirmação e disponibilidade de stock.", ln=True)
    pdf.cell(0, 10, "Rua Dr. Roberto Frias s/n, 4200-465 Porto", ln=True)
    pdf.cell(0, 10, "scitech.bestporto.org", ln=True)
    pdf.cell(0, 10, "+351 912345678", ln=True)
    
    # Salva o PDF
    pdf.output("Nota_de_Encomenda_SciTeCh24.pdf")
    print("Nota de encomenda gerada com sucesso: Nota_de_Encomenda_SciTeCh24.pdf")

# Função principal para processar pedidos e gerar nota de encomenda para o fornecedor
def main():

    orders_df = pd.read_excel("./output.xlsx")

    
    # Agregar materiais de todas as encomendas
    # aggregated_materials = aggregate_materials(orders_df)
    # total_cost = calculate_total_material_cost(aggregated_materials)
    
    # Gera o PDF da nota de encomenda para o fornecedor
    
    generate_supplier_order_pdf(AGGREGATED_MATERIALS, TOTAL_COST)

if __name__ == "__main__":
    main()
