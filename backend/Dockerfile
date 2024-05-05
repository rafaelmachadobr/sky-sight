# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install build tools
RUN apt-get update \
    && apt-get install -y gcc netcat libgdal-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# update pip
RUN pip install --upgrade pip

# install Poetry
RUN pip install poetry

# copy project
COPY backend/ .

# install dependencies
RUN poetry install

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
