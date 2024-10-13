# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set environment variables to avoid Python writing .pyc files and to enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the working directory
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Collect static files


# Run database migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Run the application
CMD ["python", "manage.py", "runserver"]

