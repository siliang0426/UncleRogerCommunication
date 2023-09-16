# Use Python 3.8 as a base image
FROM python:3.8

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Create a working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application
COPY . /app/

# Run Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
