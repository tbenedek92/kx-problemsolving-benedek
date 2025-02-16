# Distributed Service Assembly Documentation

## Folder Structure
```
service_assembly/
│── gateway_service/            # Gateway Service (FastAPI)
│   ├── app.py                  # Gateway service application logic
│   ├── Dockerfile              # Dockerfile for gateway service
│   ├── requirements.txt        # Dependencies
│   ├── tests/                  # Unit tests
│   │   ├── test_gateway.py     # Test cases for gateway service
│── storage_service/            # Storage Service (FastAPI)
│   ├── app.py                  # Storage service application logic
│   ├── Dockerfile              # Dockerfile for storage service
│   ├── requirements.txt        # Dependencies
│── docker-compose.yml          # Orchestrates services
│── Makefile                    # Provides easy local deployment and testing
```


## Services

### 1. Gateway Service
- **Description:**
  - Acts as the main interface 
  - Implements round-robin load balancing 
  - Expects list of storage services as environment variable
- **Endpoints:**
  - `GET /status` → Returns the status of all storage services.
  - `GET /data` → Fetches data from the next available storage service.
- **Limitations:**
  - If all storage services fail, requests will be rejected with a 503 error.

### **2. Storage Service**
- **Description:**
  - Stores and serves **dummy data** in-memory.
- **Endpoints:**
  - `GET /data` → Returns dummy data.
  - `GET /health` → Returns status (available/unavailable).
- **Limitations:**
  - No test coverage, as this serves only dummy data


## Deployment
### Prerequisites:
**Docker** and **Docker Compose** installed.

### 1. Deploy the Services (test and build)
```bash
make deploy
```

### 2. Destroy deployment
```bash
make clean
```

---

## Future Improvements

- Currenly only local deployments are supported. To mitigate it:
    - Implement a CI pipeline (test, lint, build, push, scan)
    - Deploy to a production ready environment
- Replace custom gateway service with a reverse proxy (e.g.: nginx)
