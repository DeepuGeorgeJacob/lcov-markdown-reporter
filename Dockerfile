# Use a minimal, secure base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy dependencies file and install them first
#COPY requirements.txt /app/requirements.txt
#RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the Python script and the entrypoint script
COPY main.py /app/main.py
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint for the container
ENTRYPOINT ["/entrypoint.sh"]