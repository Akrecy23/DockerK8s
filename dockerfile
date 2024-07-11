# Use the official Python 3.12 image as a base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /django-app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY ./dock ./dock

#Specify the default command to run the application
CMD ["python", "./dock/manage.py", "runserver", "0.0.0.0:8000"]
