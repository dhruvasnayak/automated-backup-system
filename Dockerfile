# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy everything except the backup directory to the container
COPY . .

# Install any necessary packages
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Run the app.py script when the container launches
CMD ["python", "app.py"]
