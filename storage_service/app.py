from fastapi import FastAPI
import uvicorn
import os

SERVICE_NAME = os.environ.get("SERVICE_NAME", "storage_service")

app = FastAPI()

# Dummy data
data = {"message": f"Hello from {SERVICE_NAME}"}

@app.get("/data")
async def get_data():
    return data

@app.get("/health")
async def health_check():
    return {"status": "available"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
