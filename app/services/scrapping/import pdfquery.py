import pdfquery

#no funcionala libreria, no la reconoce
pdf=pdfquery.PDFQuery("C:\\Users\\Administrator\\Repos\\last-dance\\app\\services\\scrapping\\CONTABILIDAD1.pdf")
pdf.load(8)
tabla=pdf.extract([
    ('with_parent','LTPage[pageid="4"]'), 
    ('tabla','LTTextBoxHorizontal')
])
print(tabla)