#!/bin/bash

# Development script for running Mastermind application without docker-compose
# Usage: ./dev.sh
# Make executable: chmod +x dev.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Process tracking
BACKEND_PID=""
FRONTEND_PID=""
DOCKERD_STARTED=0

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}Shutting down services...${NC}"
    
    # Kill backend process
    if [ -n "$BACKEND_PID" ]; then
        echo -e "${BLUE}Stopping backend (PID: $BACKEND_PID)...${NC}"
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    # Kill frontend process
    if [ -n "$FRONTEND_PID" ]; then
        echo -e "${BLUE}Stopping frontend (PID: $FRONTEND_PID)...${NC}"
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    # Stop PostgreSQL container
    echo -e "${BLUE}Stopping PostgreSQL container...${NC}"
    docker stop mastermind_db 2>/dev/null || true
    
    echo -e "${GREEN}Cleanup complete!${NC}"
    exit 0
}

# Set trap for cleanup on script exit
trap cleanup EXIT INT TERM

# Function to check if a port is in use
check_port() {
    local port=$1
    local process_info
    
    # Try lsof first (more common)
    if command -v lsof &> /dev/null; then
        process_info=$(lsof -i :$port -t 2>/dev/null | head -n 1)
        if [ -n "$process_info" ]; then
            local pid=$process_info
            local process_name=$(ps -p $pid -o comm= 2>/dev/null || echo "unknown")
            echo -e "${RED}ERROR: Port $port is already in use!${NC}"
            echo -e "${RED}  Process: $process_name (PID: $pid)${NC}"
            echo -e "${YELLOW}  Please stop the process using: kill $pid${NC}"
            return 1
        fi
    # Fallback to ss
    elif command -v ss &> /dev/null; then
        if ss -tuln | grep -q ":$port "; then
            echo -e "${RED}ERROR: Port $port is already in use!${NC}"
            echo -e "${YELLOW}  Run 'ss -tulnp | grep :$port' to identify the process${NC}"
            return 1
        fi
    # Fallback to netstat
    elif command -v netstat &> /dev/null; then
        if netstat -tuln | grep -q ":$port "; then
            echo -e "${RED}ERROR: Port $port is already in use!${NC}"
            echo -e "${YELLOW}  Run 'netstat -tulnp | grep :$port' to identify the process${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}WARNING: Cannot check port availability (lsof, ss, and netstat not found)${NC}"
    fi
    
    return 0
}

# Function to check all required ports
check_ports() {
    echo -e "${BLUE}Checking port availability...${NC}"
    local ports_ok=true
    
    if ! check_port 5432; then
        ports_ok=false
    fi
    
    if ! check_port 8000; then
        ports_ok=false
    fi
    
    if ! check_port 5173; then
        ports_ok=false
    fi
    
    if [ "$ports_ok" = false ]; then
        echo -e "${RED}Cannot start services due to port conflicts. Exiting.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ All required ports are available${NC}"
}

# Function to check and start Docker daemon
check_docker() {
    echo -e "${BLUE}Checking Docker daemon...${NC}"
    
    if docker ps &> /dev/null; then
        echo -e "${GREEN}✓ Docker daemon is running${NC}"
        return 0
    fi
    
    echo -e "${YELLOW}Docker daemon is not running. Starting dockerd...${NC}"
    echo -e "${YELLOW}You may be prompted for your sudo password.${NC}"
    
    # Start dockerd in background
    sudo dockerd > /tmp/dockerd.log 2>&1 &
    DOCKERD_STARTED=1
    
    # Wait for Docker to be ready (max 30 seconds)
    local timeout=30
    local elapsed=0
    
    while [ $elapsed -lt $timeout ]; do
        if docker ps &> /dev/null; then
            echo -e "${GREEN}✓ Docker daemon started successfully${NC}"
            return 0
        fi
        sleep 1
        elapsed=$((elapsed + 1))
        echo -n "."
    done
    
    echo -e "\n${RED}ERROR: Docker daemon failed to start within $timeout seconds${NC}"
    echo -e "${YELLOW}Check logs at: /tmp/dockerd.log${NC}"
    exit 1
}

# Function to manage PostgreSQL container
setup_postgres() {
    echo -e "${BLUE}Setting up PostgreSQL container...${NC}"
    
    # Check if container exists
    if docker ps -a --format '{{.Names}}' | grep -q '^mastermind_db$'; then
        # Container exists, check if it's running
        if docker ps --format '{{.Names}}' | grep -q '^mastermind_db$'; then
            echo -e "${GREEN}✓ PostgreSQL container is already running${NC}"
        else
            echo -e "${YELLOW}Starting existing PostgreSQL container...${NC}"
            docker start mastermind_db
        fi
    else
        # Create new container with persistent volume
        echo -e "${YELLOW}Creating PostgreSQL container with persistent volume...${NC}"
        docker run -d \
            --name mastermind_db \
            -e POSTGRES_USER=mastermind \
            -e POSTGRES_PASSWORD=mastermind_dev \
            -e POSTGRES_DB=mastermind \
            -p 5432:5432 \
            -v mastermind_db_data:/var/lib/postgresql/data \
            postgres:15-alpine
    fi
    
    # Wait for PostgreSQL to be ready
    echo -e "${BLUE}Waiting for PostgreSQL to be ready...${NC}"
    local timeout=30
    local elapsed=0
    
    while [ $elapsed -lt $timeout ]; do
        if docker exec mastermind_db pg_isready -U mastermind &> /dev/null; then
            echo -e "${GREEN}✓ PostgreSQL is ready${NC}"
            return 0
        fi
        sleep 1
        elapsed=$((elapsed + 1))
        echo -n "."
    done
    
    echo -e "\n${RED}ERROR: PostgreSQL failed to become ready within $timeout seconds${NC}"
    exit 1
}

# Function to setup Python virtual environment
setup_python_env() {
    echo -e "${BLUE}Setting up Python environment...${NC}"
    
    # Create venv if it doesn't exist
    if [ ! -d ".venv" ]; then
        echo -e "${YELLOW}Creating Python virtual environment...${NC}"
        python3 -m venv .venv
        
        echo -e "${YELLOW}Installing Python dependencies...${NC}"
        source .venv/bin/activate
        pip install --upgrade pip > /dev/null
        pip install -e . > /dev/null
    else
        echo -e "${GREEN}✓ Virtual environment exists${NC}"
        source .venv/bin/activate
    fi
    
    # Always run migrations and seeding
    echo -e "${BLUE}Running database migrations...${NC}"
    export DATABASE_URL="postgresql+asyncpg://mastermind:mastermind_dev@localhost:5432/mastermind"
    alembic upgrade head
    
    echo -e "${BLUE}Seeding database with AI users...${NC}"
    python scripts/seed_ai_users.py
    
    echo -e "${GREEN}✓ Python environment ready${NC}"
}

# Function to setup Node.js environment
setup_node_env() {
    echo -e "${BLUE}Setting up Node.js environment...${NC}"
    
    cd frontend
    
    # Install npm dependencies if node_modules doesn't exist
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Installing npm dependencies...${NC}"
        npm install
    else
        echo -e "${GREEN}✓ Node modules exist${NC}"
    fi
    
    cd ..
    echo -e "${GREEN}✓ Node.js environment ready${NC}"
}

# Function to start backend server
start_backend() {
    echo -e "${BLUE}Starting backend server...${NC}"
    
    # Ensure venv is activated and set DATABASE_URL
    source .venv/bin/activate
    export DATABASE_URL="postgresql+asyncpg://mastermind:mastermind_dev@localhost:5432/mastermind"
    export CORS_ORIGINS="http://localhost:3000,http://localhost:5173"
    
    # Start uvicorn in background (stderr to separate file for debugging)
    uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload > /tmp/mastermind_backend.log 2> /tmp/mastermind_backend_error.log &
    BACKEND_PID=$!
    
    # Wait a moment to check if it started successfully
    sleep 2
    if ps -p $BACKEND_PID > /dev/null; then
        echo -e "${GREEN}✓ Backend server started (PID: $BACKEND_PID)${NC}"
        echo -e "${GREEN}  Backend logs: /tmp/mastermind_backend.log${NC}"
        echo -e "${GREEN}  Backend errors: /tmp/mastermind_backend_error.log${NC}"
    else
        echo -e "${RED}ERROR: Backend failed to start${NC}"
        echo -e "${YELLOW}Check logs at: /tmp/mastermind_backend.log${NC}"
        echo -e "${YELLOW}Check errors at: /tmp/mastermind_backend_error.log${NC}"
        exit 1
    fi
}

# Function to start frontend server
start_frontend() {
    echo -e "${BLUE}Starting frontend server...${NC}"
    
    cd frontend
    npm run dev > /tmp/mastermind_frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    
    # Wait a moment to check if it started successfully
    sleep 2
    if ps -p $FRONTEND_PID > /dev/null; then
        echo -e "${GREEN}✓ Frontend server started (PID: $FRONTEND_PID)${NC}"
        echo -e "${GREEN}  Frontend logs: /tmp/mastermind_frontend.log${NC}"
    else
        echo -e "${RED}ERROR: Frontend failed to start${NC}"
        echo -e "${YELLOW}Check logs at: /tmp/mastermind_frontend.log${NC}"
        exit 1
    fi
}

# Main execution
main() {
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}Mastermind Development Server${NC}"
    echo -e "${GREEN}================================${NC}\n"
    
    # Step 1: Check ports
    check_ports
    
    # Step 2: Ensure Docker is running
    check_docker
    
    # Step 3: Setup PostgreSQL
    setup_postgres
    
    # Step 4: Setup Python environment and run migrations
    setup_python_env
    
    # Step 5: Setup Node.js environment
    setup_node_env
    
    # Step 6: Start backend server
    start_backend
    
    # Step 7: Start frontend server
    start_frontend
    
    # Success message
    echo -e "\n${GREEN}================================${NC}"
    echo -e "${GREEN}All services started successfully!${NC}"
    echo -e "${GREEN}================================${NC}\n"
    echo -e "${BLUE}Frontend:${NC}    http://localhost:5173"
    echo -e "${BLUE}Backend API:${NC} http://localhost:8000"
    echo -e "${BLUE}API Docs:${NC}    http://localhost:8000/docs"
    echo -e "\n${YELLOW}Press Ctrl+C to stop all services${NC}\n"
    
    # Wait for user interrupt
    wait
}

# Run main function
main
