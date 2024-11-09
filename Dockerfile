FROM python:3.9-slim

# Set work directory
WORKDIR /consumer

# Install dependencies
COPY requirements.txt /consumer/
RUN pip install --no-cache-dir -r requirements.txt

# Copy consumer script
COPY consumer.py /consumer/

# Run the consumer script
CMD ["python", "consumer.py"]