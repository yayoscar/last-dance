import requests
from bs4 import BeautifulSoup

url='http://127.0.0.1:5500/app/services/scrapping/SISEEMS%20-%20Acreditaci%C3%B3n.html'
page=requests.get(url)
soup=BeautifulSoup(page.text,'html.parser')

seccion=soup.find('div',id='ctl0_Main_panelAlumnos')
tabla=seccion.find('table')
encabezados=[
    "NO","NO CONTROL","NOMBRE",
    "PARCIAL_1","PARCIAL_2","PARCIAL_3",
    "ASISTENCIA_1","ASISTENCIA_2","ASISTENCIA_3",
    "PROMEDIO","ASISTENCIAS","T. A.","FIRMADO"]
datos=[]
filas=tabla.find_all('tr')[1:]


for fila in filas:
    celdas=fila.find_all('td')
    valores=[celda.text.strip() for celda in celdas]
    if valores:
        fila_dict=dict(zip(encabezados,valores))
        datos.append(fila_dict)
for fila in datos:
    print(fila)
#chikis