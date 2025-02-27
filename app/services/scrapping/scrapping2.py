import xlwings as xw

# Ruta del archivo
file_path="app/services/scrapping/1A-M.xlsx"

wb=xw.Book(file_path)
sheet=wb.sheets[0]


redi = {}
carrera=sheet['A7'].value.split(':')
carrera=carrera[-1].strip()
redi["carrera"]=carrera

semestre=sheet['A8'].value.split(':')
semestre=semestre[-1].strip()
redi["semestre"]=semestre

fila = 13
alumnos=[]
while True:
    dict_alumno={}
    num_control = sheet['B'+str(fila)].value
    if(num_control is None):
        break
    dict_alumno['num_control']=str(num_control)
    fila+=1
    alumnos.append(dict_alumno)
    
redi['alumnos']=alumnos

wb.close()

print(redi)