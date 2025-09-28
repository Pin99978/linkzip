# 1. Base Image
# We use a slim image to keep the size small.
FROM python:3.12-slim

# 2. Set Environment Variables
# Prevents Python from writing pyc files to disc (equivalent to python -B)
ENV PYTHONDONTWRITEBYTECODE=1
# Ensures Python output is sent straight to the terminal without buffering
ENV PYTHONUNBUFFERED=1

# 3. Set Work Directory
WORKDIR /app

# 4. Install Dependencies
# Copy the requirements file first to leverage Docker layer caching.
# If requirements.txt doesn't change, Docker won't re-run this layer.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy Application Code
COPY ./src /app/src

# 6. Expose Port
# Make port 8000 available to the world outside this container.
EXPOSE 8000

# 7. Run Application
# Command to run the app using uvicorn.
# --host 0.0.0.0 is crucial to allow connections from outside the container.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
