# Use Python 3.12 as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app to the container
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Define the command to run the Flask app
CMD ["flask", "run"]