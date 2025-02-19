import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="localhost", port=3200, reload=True,log_level="debug")