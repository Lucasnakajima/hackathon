from fpdf import FPDF
from datetime import datetime
import pandas as pd 
import os
from PyPDF2 import PdfReader, PdfWriter
import io

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

def generate_supplier_order_pdf(aggregated_materials, total_cost):
    try:
        # Cria um PDF temporário com apenas a tabela
        temp_pdf = FPDF()
        temp_pdf.add_page()
        
        # Define posição inicial da tabela
        start_x = 24
        start_y = 120
        temp_pdf.set_xy(start_x, start_y)
        
        # Larguras das colunas
        col_widths = {
            'artigo': 35,
            'quantidade': 45,
            'preco': 36,
            'subtotal': 45
        }
        
        # Cabeçalho da tabela
        temp_pdf.set_font("Helvetica", "B", 10)
        temp_pdf.set_text_color(0, 0, 0)  # Cor do texto preta
        
        # Dados da tabela
        temp_pdf.set_font("Helvetica", "", 10)
        for material, amount in aggregated_materials.items():
            temp_pdf.set_x(start_x)  # Garante que cada linha comece no mesmo x
            unit_price = MATERIAL_PRICES.get(material, 0)
            subtotal = amount * unit_price
            temp_pdf.cell(col_widths['artigo'], 10, material.capitalize(), border=1)
            temp_pdf.cell(col_widths['preco'], 10, f"EUR {unit_price:.2f}", border=1, align='C')
            temp_pdf.cell(col_widths['quantidade'], 10, f"{amount:.0f}", border=1, align='C')
            temp_pdf.cell(col_widths['subtotal'], 10, f"EUR {subtotal:.2f}", border=1, align='C')
            temp_pdf.ln(10)
        
        # Total
        temp_pdf.set_x(start_x)
        temp_pdf.set_font("Helvetica", "B", 10)
        total_width = col_widths['artigo'] + col_widths['quantidade'] + col_widths['preco']
        temp_pdf.cell(total_width, 10, "Total:", border=1)
        temp_pdf.cell(col_widths['subtotal'], 10, f"EUR {total_cost:.2f}", border=1, align='C')
        
        # Salva o PDF temporário em memória
        pdf_bytes = io.BytesIO()
        temp_pdf.output(pdf_bytes)
        pdf_bytes.seek(0)
        
        # Abre o PDF template
        reader = PdfReader("Nota de encomenda.pdf")
        writer = PdfWriter()
        
        # Pega a primeira página do template
        page = reader.pages[0]
        
        # Adiciona a tabela por cima
        overlay = PdfReader(pdf_bytes)
        page.merge_page(overlay.pages[0])
        
        # Adiciona a página modificada ao writer
        writer.add_page(page)
        
        # Salva o PDF final
        with open("Nota_de_Encomenda_SciTeCh24.pdf", "wb") as output_file:
            writer.write(output_file)
            
        print("Nota de encomenda gerada com sucesso: Nota_de_Encomenda_SciTeCh24.pdf")
            
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        print("Certifique-se de que o arquivo 'Nota de encomenda.pdf' existe no diretório")

def main():
    orders_df = pd.read_excel("./output.xlsx")
    generate_supplier_order_pdf(AGGREGATED_MATERIALS, TOTAL_COST)

if __name__ == "__main__":
    main()
