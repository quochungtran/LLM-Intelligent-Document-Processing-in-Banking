FROM python:3.10.12-slim-bullseye

RUN pip install --upgrade pip

WORKDIR /usr/src/app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app/
COPY entrypoint.sh /usr/src/app/
COPY ./requirements.txt /usr/src/app/

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
