FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Ensure standard output is not buffered
ENV PYTHONUNBUFFERED=1

# Install git required for installing packages from git repositories
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . .

# Expose the correct port for the application
EXPOSE 8000

# Start the FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
