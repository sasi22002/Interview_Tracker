# Pull the official Python image
FROM python:3.9-slim

# Set the working directory
# WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the project files into the container
COPY . .


# Run the Django development server (replace with production server if needed)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
