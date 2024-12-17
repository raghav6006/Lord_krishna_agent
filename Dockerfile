# Use Python 3.12 slim version as the base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Install dependencies
RUN  pip install -r requirements.txt

# Set environment variable for OpenAI API key
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["python", "krishna4.py"]
