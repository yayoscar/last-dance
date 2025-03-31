import pdfquery

# Cargar el PDF
pdf = pdfquery.PDFQuery("archivo.pdf")
pdf.load(4)  # Cargar la página 4

# Extraer todos los elementos de la tabla
tabla = pdf.extract([
    ('with_parent', 'LTPage[pageid="4"]'),  # Buscar en la página 4
    ('tabla', 'LTTextBoxHorizontal')  # Extraer texto de los cuadros horizontales
])

# Mostrar los datos
for elemento in tabla['tabla']:
    print(elemento.text)
