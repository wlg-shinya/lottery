# FROM node:20.9.0 as builder
# WORKDIR /usr/src/app
# COPY . /usr/src/app
# ENV NODE_ENV=development
# RUN npm install
# RUN npm run build
# RUN npm run serve:build

# FROM node:20.9.0-alpine as prod
# WORKDIR /usr/src/app
# COPY --from=builder /usr/src/app /usr/src/app
# ENV NODE_ENV=production
# RUN npm install
# RUN npm install -g http-server

FROM python:3.12-alpine as srv
WORKDIR /usr/src/app
COPY ./srv /usr/src/app
RUN pip install poetry alembic
RUN poetry install
RUN alembic upgrade head

FROM openjdk:11 as openapi-generate
RUN apt update
RUN apt install -y nodejs npm
RUN npm install -g n
RUN n 20.9.0
RUN apt purge -y nodejs npm
RUN apt autoremove -y
WORKDIR /usr/src/app
COPY . /usr/src/app
ENV NODE_ENV=development
RUN npm install