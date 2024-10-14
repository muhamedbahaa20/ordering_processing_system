# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the working directory
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Collect static files


# Run database migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Run the application
CMD ["python", "manage.py", "runserver","0.0.0.0:8000"]

