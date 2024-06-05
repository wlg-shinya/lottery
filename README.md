# lottery

## Project setup

```
$ npm install
$ cd ./srv
$ poetry install
```

## Development

### DB startup

```
$ docker-compose up db
```

### Build and run

```
$ npm run dev && npm run srv
```

### Build and run for production

```
$ npm run build && npm run preview && npm run srv
```

### DB migration

After edit 'srv/api/models.py'

```
$ cd ./srv
$ alembic revision --autogenerate
$ alembic upgrade head
```

### OpenAPI update

After edit below 'srv/api/'

```
$ npm run openapi:download
$ docker-compose up openapi_generate --build
```

## Deploy

```
$ npm run clean && docker-compose up --build
```
