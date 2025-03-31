import pdfquery

#no funcionala libreria, no la reconoce
pdf=pdfquery.PDFQuery("app\services\scrapping\_CIENCIAS_DE_DATOS_E_INFORMACION1.pdf")
pdf.load(8)
tabla=pdf.extract([
    ('with_parent','LTPage[pageid="4"]'), 
    ('tabla','LTTextBoxHorizontal')
])
