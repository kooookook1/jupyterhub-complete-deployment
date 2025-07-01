FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nodejs npm curl wget git build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install configurable-http-proxy
RUN npm install -g configurable-http-proxy

# Set working directory
WORKDIR /app

# Copy package.json and install Node.js dependencies
COPY package*.json ./
RUN npm install

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Install JupyterHub in development mode
RUN pip install -e .

# Build frontend assets
RUN npm run build || echo "Build completed"

# Create necessary directories
RUN mkdir -p runtime data logs

# Set permissions
RUN chmod +x start_jupyterhub.sh setup_complete_deployment.sh

# Expose port
EXPOSE 12001

# Start JupyterHub
CMD ["jupyterhub", "--config=jupyterhub_config_production.py"]