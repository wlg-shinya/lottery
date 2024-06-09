FROM node:20.9.0 as frontend-build
WORKDIR /usr/src/app
COPY . /usr/src/app
ENV NODE_ENV=development
RUN npm install
RUN npm run build

FROM node:20.9.0-alpine as frontend
WORKDIR /usr/src/app
COPY --from=frontend-build /usr/src/app/dist/ /usr/src/app/package.json /usr/src/app/
ENV NODE_ENV=production
RUN npm install
RUN npm install -g http-server

FROM python:3.12-alpine as backend
WORKDIR /usr/src/app
COPY ./srv /usr/src/app
RUN pip install poetry
RUN poetry install

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