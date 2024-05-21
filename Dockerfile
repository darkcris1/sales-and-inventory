FROM python:3.10.12-alpine

# Set the working directory in the container
WORKDIR /sales-and-inventory-management

# Copy the current directory contents into the container at /sales-and-inventory-management
COPY . /sales-and-inventory-management

# Upgrade pip
RUN pip install --upgrade pip

# Install the dependencies
RUN pip install -r requirements.txt

# Install Gunicorn separately
RUN pip install gunicorn

# Expose the port that the app will run on
EXPOSE 8000

# Run database migrations
RUN python manage.py migrate

# Load initial data
RUN python manage.py loaddata fixtures/*.json

# Command to run the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "InventoryMS.wsgi:application"]
