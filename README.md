# くじ引きメーカー(β) (lottery)

https://lottery.welovegamesinc.com/#/

自分の好きなくじ引きを作ることができます。作ったくじ引きをシェアすることもできます

## At first setup

```
echo SMTP_PASSWORD=\"YourGmailAppPassword\" > srv/.env.local
```

## Development

## Setup

```
npm install
cd ./srv
poetry install
```

### DB's docker startup

```
docker compose up db
```

### Backend build and run

```
npm run srv
```

### Frontend build and run

```
npm run dev
```

### Backend test

First time only

```
docker compose -f docker-compose-db-test.yml up
```

Main process

```
npm run srv:test
```

### Backend's docker startup

```
docker compose up backend --build
```

### Frontend build and run for production

```
npm run build && npm run preview
```

### DB migration

After edit 'srv/api/models.py'

```
npm run db:migration
```

### OpenAPI update

After edit below 'srv/api/' and backend is running by 'npm run srv'

```
npm run openapi:update
```

## Deploy

```
docker compose up --build
```
