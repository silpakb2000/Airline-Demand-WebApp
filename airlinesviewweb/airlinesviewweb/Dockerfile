# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy project files into container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
