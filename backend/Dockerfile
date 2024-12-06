FROM python:3.10.12-slim-bullseye

WORKDIR /qhung/src/app

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /qhung/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /qhung/src/app/
