# 1: Start Docker kernel + Python
FROM python:3.12.6-slim-bullseye

# 2: ENV: Show logs
ENV PYTHONUNBUFFERED=1

# 3: Update kernel + install dependencies
RUN apt-get update && apt-get -y install gcc libpq-dev

# 4: Create project folder
WORKDIR /app

# 5: Copy requirements file
COPY requirements.txt /app/requirements.txt

# 6: Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# 7: Copy project code into the container
COPY . /app/

# 8: Default command (can be overridden by docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]