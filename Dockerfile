# Use the official Python 3.10 image as the base
FROM python:3.10

# Create and set a working directory in a single step
WORKDIR /retrieval

# It's a best practice to not run the application as the root user
# User 'nobody' is already available in the base image
# USER nobody

# Copy only the requirements.txt initially to leverage Docker cache
# COPY --chown=nobody:nobody requirements.txt ./
COPY requirements.txt .

# Install the dependencies
# Using --no-cache-dir for pip to keep the image size down
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install -r requirements.txt

# Copy the rest of the application code with the appropriate ownership
# COPY --chown=nobody:nobody . .
COPY . .


# Expose the application's port
# EXPOSE 8080

# Run the application with a non-root user for security
CMD ["python", "main.py"]