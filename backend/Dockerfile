FROM python:3.10.12-slim-bullseye

RUN apt update -y \
    && apt-get install \
        python3-dev \
        default-libmysqlclient-dev \
        build-essential \
        pkg-config -y \
    && apt-get clean

# Set working directory
WORKDIR /appllm

# Copy source code
# copy content of src folder to appllm/src folder
COPY src /appllm/src 

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="${PYTHONPATH}:/appllm:/appllm/src"

# Expose port
EXPOSE 8081

# Copy and install dependencies
COPY requirements.txt /appllm
COPY requirements_sql_db.txt /appllm

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r requirements_sql_db.txt


# Run the application
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8081", "--workers", "2", "--log-level", "info"]