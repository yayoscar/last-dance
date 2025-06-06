import pdfquery

# Cargar el PDF
pdf_path = "app\\services\\scrapping\CONTABILIDAD1.pdf"  # Asegúrate de que el archivo esté en el mismo directorio o coloca la ruta completa
pdf = pdfquery.PDFQuery(pdf_path)
pdf.load()

# Función para extraer texto de cada página
def extract_text_from_pdf(pdf):
    extracted_data = []
    for page_num in range(len(pdf.tree.findall('.//LTPage'))):
        page = pdf.pq(f'LTPage[page_index="{page_num}"]')
        text_elements = page('LTTextBoxHorizontal')
        
        for element in text_elements:
            text = element.text.strip()
            if text:  # Evita agregar elementos vacíos
                extracted_data.append(text)
    return extracted_data

# Obtener el texto del documento
extracted_text = extract_text_from_pdf(pdf)

# Filtrar la información que contenga términos clave como "carrera", "materia" y "módulo"
filtered_data = [line for line in extracted_text if any(keyword in line.lower() for keyword in ["carrera", "materia", "módulo"])]

# Imprimir los resultados
for line in filtered_data:
    print(line)
