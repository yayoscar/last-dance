import xlwings as xw

file_path = "app/services/scrapping/1A-M.xlsx"

wb = xw.Book(file_path)
sheet_names = [sheet.name for sheet in wb.sheets]
print("Hojas disponibles:", sheet_names)

sheet = wb.sheets[0]

# Leer la celda A7
valor = sheet.range("A7").value
print("Valor en A7:", valor)

data = sheet.range("C13:C68").value

for row in data:
    print(row)

wb.close()

