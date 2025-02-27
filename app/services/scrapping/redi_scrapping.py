import xlwings as xw
file_path="app\services\scrapping\Programación.xlsx"

def funcion(file):
    wb=xw.Book(file_path)
    sheet=wb.sheets[0]
    redi = {}
    carrera=sheet['A7'].value.split(':')
    carrera=carrera[-1].strip()
    redi["carrera"]=carrera

    semestre=sheet['A8'].value.split(':')
    semestre=semestre[-1].strip()
    redi["semestre"]=semestre
    fila=13
    num_control=[]

    while True:
        fila_b={}
        nums_control = sheet['B'+str(fila)].value
        if nums_control is None:
            fila=13
            break
        fila_b['Num_control']=int(nums_control)
        fila+=1
        num_control.append(fila_b)
    
    redi['fila_b']=num_control

    nombre=[]
    while True:
        fila_c={}
        nombres = sheet['C'+str(fila)].value
    
        if nombres is None:
            fila=13
            break
        fila_c['Nombres']=str(nombres)
        fila+=1
        nombre.append(fila_c)
    
    redi['fila_c']=nombre

    curp=[]
    while True:
        fila_d={}
        curps = sheet['D'+str(fila)].value
    
        if curps is None:
            fila=13
            break
        fila_d['Curp']=str(curps)
        fila+=1
        curp.append(fila_d)
    
    redi['fila_d']=curp

    genero=[]

    while True:
        fila_e={}
        generos=sheet['E'+str(fila)].value

        if generos is None:
            fila=13
            break
        fila_e['Genero']=str(generos)
        fila+=1
        genero.append(fila_e)

    redi['fila_e']=genero


    edad=[]
    while True:
        fila_f={}
        edades=sheet['F'+str(fila)].value

        if edades is None:
            fila=13
            break
        fila_f['Edad']=str(edades)
        fila+=1
        edad.append(fila_f)

    redi['fila_f']=edad

    plant_proc=[]
    while True:
        fila_g={}
        plants_proc=sheet['G'+str(fila)].value
        cont=sheet['B'+str(fila)].value

        if cont is None:
            fila=13
            break
        fila_g['Plant']=str(plants_proc)
        fila+=1
        plant_proc.append(fila_g)

    redi['fila_g']=plant_proc


    cod_obs=[]
    while True:
        fila_h={}
        cods_obs=sheet['H'+str(fila)].value
        cont2=sheet['B'+str(fila)].value

        if cont2 is None:
            fila=13
            break
        fila_g['Cod_obs']=str(cods_obs)
        fila+=1
        cod_obs.append(fila_h)

    redi['fila_h']=cod_obs
    print(redi)
    wb.close()

funcion(file_path)