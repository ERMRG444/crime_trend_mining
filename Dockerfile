FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Expose port
EXPOSE 8080

# Run the application (Production WSGI replacement usually requires gunicorn/eventlet, 
# but for demo simplicity with flask-socketio, we can run app.py or use gunicorn with eventlet)
CMD ["python", "app.py"]
