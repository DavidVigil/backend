FROM python:3-alpine

# Set environment variables to ensure output is sent straight to the terminal without buffering
ENV PYTHONUNBUFFERED=1

# Set environment variables for MongoDB
ENV MONGODB_USER=fimarket
ENV MONGODB_PASS=awesomefimarketpass123
ENV MONGODB_HOST=database

# Update pip to the latest version
RUN pip install --upgrade pip

# Install Flask and Marshmallow
RUN pip install Flask Marshmallow

# Create a directory for the application
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY app.py /app
# to do: copy flask files

# Expose port 5000 for Flask
EXPOSE 5000

# Set the entry point to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
