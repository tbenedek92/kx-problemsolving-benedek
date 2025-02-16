from fastapi import FastAPI, HTTPException
import requests
import os
import itertools
import logging
import uvicorn

logger = logging.getLogger("uvicorn")

def get_storage_services():
    """Reads and parses storage services from the environment variable."""
    storage_services_env = os.getenv("STORAGE_SERVICES", "")
    storage_services_list = [url.strip() for url in storage_services_env.split(",") if url.strip()]
    services = {f"storage_{i+1}": f"http://{url}" for i, url in enumerate(storage_services_list)}
    
    if not services:
        logger.warning("No storage services configured.")
    else:
        logger.info(f"Configured storage services: {list(services.values())}")
    
    return services

STORAGE_SERVICES = get_storage_services()
app = FastAPI()
service_cycle = itertools.cycle(STORAGE_SERVICES.values())

@app.get("/status")
async def check_status():
    """Checks the availability of all storage services."""
    status = {}
    for service_name, service_url in STORAGE_SERVICES.items():
        try:
            response = requests.get(f"{service_url}/health", timeout=2)
            status[service_name] = "available" if response.status_code == 200 else "unavailable"
        except requests.RequestException as e:
            logger.warning(f"Service {service_name} ({service_url}) is unavailable: {e}")
            status[service_name] = "unavailable"
    return status

@app.get("/data")
async def get_data():
    """Fetches data from the next available storage service using round robin."""
    for _ in range(len(STORAGE_SERVICES)):
        service_url = next(service_cycle)
        try:
            response = requests.get(f"{service_url}/data", timeout=2)
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Service {service_url} returned status {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Failed to fetch data from {service_url}: {e}")
            continue
    
    logger.error("No storage services are currently available.")
    raise HTTPException(status_code=503, detail="No storage services available")

if __name__ == "__main__":
    logger.info("Starting Gateway service")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
