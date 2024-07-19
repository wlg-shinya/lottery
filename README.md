# lottery

## Project setup

```
$ npm install
$ cd ./srv
$ poetry install
$ echo SMTP_PASSWORD=\"YourGmailAppPassword\" > .env.local
```

## Development

### DB's docker startup

```
$ docker compose up db
```

### Backend build and run

```
$ npm run srv
```

### Frontend build and run

```
$ npm run dev
```

### Backend test

First time only

```
$ docker compose -f docker-compose-db-test.yml up
```

Main process

```
$ npm run srv:test
```

### Backend's docker startup

```
$ docker compose up backend --build
```

### Frontend build and run for production

```
$ npm run build && npm run preview
```

### DB migration

After edit 'srv/api/models.py'

```
$ npm run db:migration
```

### OpenAPI update

After edit below 'srv/api/' and backend is running

```
$ npm run openapi:update
```

## Deploy

```
$ npm run clean && docker compose up --build
```
