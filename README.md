 docker-compose build --no-cache
 docker-compose exec kss flask db upgrade
 docker-compose exec kss flask kss fixtures