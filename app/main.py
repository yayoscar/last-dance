import uvicorn

if __name__ == "__main__":
    print("🚀 Iniciando servidor en http://localhost:3200")
    print("📘 Documentación Swagger: http://localhost:3200/docs")
    print("🔧 Documentación ReDoc:   http://localhost:3200/redoc")
    uvicorn.run("app.app:app", host="localhost", port=3200, log_level="debug")