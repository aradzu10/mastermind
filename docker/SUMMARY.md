# docker/

Docker configuration files for containerization.

## Purpose
Contains Dockerfile and related Docker configuration for building and running the backend application in containers. Used by docker-compose for orchestrated multi-container deployment.

## Contents

### Files

- **backend.Dockerfile** - Dockerfile for building the FastAPI backend container

### Dockerfile Instructions in backend.Dockerfile

- Sets up Python 3.10 environment
- Installs system dependencies
- Copies requirements and installs Python packages
- Copies application code
- Exposes port 8000
- Sets CMD to run uvicorn server

### Functions
None (Dockerfile uses declarative syntax)

### Classes
None
