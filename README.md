# last-dance
Sistema de Reportes de Calificaciones de Control Escolar SISEEMS

# Crear Correr Primero el Entorno Virtual
python -m venv .venv
.venv\Scripts\activate


# Instalar Dependencias de Librerías
pip install -r requirements.txt

# Crear el archivo .env (Variables de Entorno)
hacer una copia .env.local
renombrarla como .env
pasar los datos de su BD

# Ejecutar Migraciones
alembic revision --autogenerate -m "init db"  
alembic upgrade head

# Ejecutar Servidor API
python -m app.main


# Instalar Librerias de FrontEnd (Una vez y cuando se informe que hay nuevos paquetes)

## ir al directorio del frontend
cd frontend

## requiere instalar nodejs
https://nodejs.org/en

## Instalar las dependencias
npm install

## Ejecutar el servidor de desarrollo
npm run dev

Documentos de Apoyo
https://drive.google.com/drive/folders/1jKSzODhhK1Oi4KV_Opf8rkMe3u5NAjJs?usp=sharing

Tablero Trello
https://trello.com/invite/b/67a4cacf66f70b9f4c08fb25/ATTI7f847c45ac130fee5067b84ed2c38b2aB3143A10/last-dance

Repositorio Github
https://github.com/yayoscar/last-dance

Diagramas DB
https://www.drawdb.app/editor?shareId=594a953231ae5f0a150e3c752fb7b0ec


##Equipos
 - Emerath
 - Limberth
 - Jade
 - Zaire
 - Ana Brenda
 - Daniela
 - Victor
 - Bianka
 
 - Andy
 - Jaime
 - Diego
 - Nain
 - Adrian
 - Pietro
 - Tagle
 - Alexandra
 
 - Alexa
 - Jaris
 - Ricardo
 - Keyla P
 - Dafne
 - Magaly
 - Isui
 - Viviana
 
 - Cristobal
 - Jairo
 - Javier
 - Aldo
 - Marco
 - Jesus
 - William
- Keyla C 
