# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install build tools
RUN apt-get update \
    && apt-get install -y gcc netcat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# install Poetry
RUN pip install poetry

# copy project
COPY . .

# install dependencies
RUN poetry install

# copy entrypoint.sh
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# command to run on container start
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
