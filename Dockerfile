# Use a minimal, secure base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the Python script and the entrypoint script
COPY main.py /app/main.py
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Install any Python dependencies here if needed (e.g., pip install requests)
# For this action, the description stated it uses only the standard library, so requirements.txt is omitted.

# Set the entrypoint for the container
ENTRYPOINT ["/entrypoint.sh"]
