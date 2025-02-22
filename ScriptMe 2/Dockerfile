# Use a lightweight Python image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the script to the container
COPY main.py /app/main.py

# Expose the necessary port
EXPOSE 17751
EXPOSE 39112
EXPOSE 36214
EXPOSE 9999

# Run the challenge script
CMD ["python", "/app/main.py"]
