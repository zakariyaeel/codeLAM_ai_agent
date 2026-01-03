# Use Python 3.9 slim for a smaller image size
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies needed for Python packages
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy your requirements file first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your project files (main.py, ui.py, agent.py, etc.)
COPY . .

# Expose the port Streamlit uses
EXPOSE 8501

# Command to run your app as you do in terminal 1
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]