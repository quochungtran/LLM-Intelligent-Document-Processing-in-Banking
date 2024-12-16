## Install dependencies
    pip install -r requirements.txt

## Run docker
    docker compose up -d

## Stop docker
    docker compose down

## Access
    docker exec -it mariadb-tiny bash
    mysql -u root -p

    CREATE DATABASE chatbot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
