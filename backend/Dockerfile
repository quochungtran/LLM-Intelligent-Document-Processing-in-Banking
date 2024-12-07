FROM python:3.10.12-slim-bullseye

WORKDIR /appllm

# copy src code into docker folder
COPY ./src /appllm/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/appllm:/appllm/src"

# expost port that the container listen this port
EXPOSE 8081

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt . 
COPY requirements_vector_db.txt . 
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install -r requirements_vector_db.txt --no-cache-dir

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8081"]
