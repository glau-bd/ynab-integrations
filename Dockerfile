# Use an official Python runtime as the base image
FROM python:3.11-bullseye as stage0

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
    POETRY_VERSION=1.5.1

# Set the working directory in the container
WORKDIR /app

# Setup dependencies
RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false

FROM stage0 as stage1
COPY . .
RUN poetry install --only main