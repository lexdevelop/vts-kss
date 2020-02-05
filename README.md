# VTS - Klijent Server Sistemi

## How to run project with docker

### Create environment file from .env.dist one and change values
```bash
cp .env.dist .env
```
For **SQLALCHEMY_DATABASE_URI** make sure that absolute path is specified, default one from .env.dist refers to /tmp directory

### Build docker container
```bash
docker-compose build --no-cache
```
This command will build application with all dependencies inside container and it will parse environment variables from .env file

Database migrations are executed in build process

Fixtures with questions and users are also executed in build process (after each container rebuild database data which are not part of the fixtures will be destroyed since we are using SQLite database which is part of the container filesystem)

Fixtures will provide 4 user accounts (username:password):

**user1**:**user1**

**user2**:**user2**

**user3**:**user3**

**user4**:**user4**

New account can be also created inside application.

### Run container
To run container execute:
```bash
docker-compose up
```
To run container in background:
```bash
docker-compose up -d
```

**Make sure that port 5000 is not already in use**

### Login inside container
To enter inside container:
```bash
docker-compose exec kss sh
```

### Shutdown container
To shutdown container:
```bash
docker-compose down
```

## Run project without docker (pipenv)

### Create environment file from .env.dist one and change values
```bash
cp .env.dist .env
```

### Install dependencies
```bash
pipenv install
```

### Open virtual environment shell
```bash
pipenv shell
```

### Run flask migrations
```bash
flask db upgrade
```

### Run flask fixtures
```bash
flask kss fixtures
```

### Run flask application
```bash
flask run
```

### Notes
Make sure that **SQLALCHEMY_DATABASE_URI** in .env file **never** use relative path like **sqlite:///app.db**

Make sure that you are using **python 3.6**