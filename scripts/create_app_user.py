#!/usr/bin/env python3
"""
Создатель пользователей приложения MongoDB
Этот скрипт создает пользователей приложения в MongoDB для разработки.
"""
import os
import sys

import pymongo

# Параметры подключения к MongoDB из переменных окружения
MONGO_HOST = os.getenv("MONGO_HOST", "127.0.0.1")
MONGO_PORT = int(os.getenv("MONGO_PORT", "27031"))
ADMIN_USER = os.getenv("MONGO_ADMIN_USER", "mongo-1")
ADMIN_PASS = os.getenv("MONGO_ADMIN_PASSWORD")
if not ADMIN_PASS:
    print("ERROR: MONGO_ADMIN_PASSWORD environment variable must be set")
    sys.exit(1)

# Конфигурация базы данных приложения и пользователя из переменных окружения
APP_DB = os.getenv("MONGO_DB", "appdb")
APP_USER = os.getenv("APP_DB_USER", "appuser")
APP_PASS = os.getenv("APP_DB_PASSWORD")
if not APP_PASS:
    print("ERROR: APP_DB_PASSWORD environment variable must be set")
    sys.exit(1)


def create_app_user():
    """Создает пользователя приложения с правами чтения/записи на базе данных appdb"""
    # Подключение к MongoDB используя учетные данные администратора
    uri = (
        f"mongodb://{ADMIN_USER}:{ADMIN_PASS}@{MONGO_HOST}:{MONGO_PORT}"
        "/admin?directConnection=true&authSource=admin"
    )
    client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
    db = client[APP_DB]

    try:
        # Создать пользователя с ролью readWrite на базе данных приложения
        db.command(
            "createUser",
            APP_USER,
            pwd=APP_PASS,
            roles=[{"role": "readWrite", "db": APP_DB}],
        )
        print(f"User '{APP_USER}' created with readWrite role on database '{APP_DB}'.")
    except pymongo.errors.OperationFailure as e:
        if "already exists" in str(e):
            print(f"User '{APP_USER}' already exists.")
        else:
            print(f"Failed to create user: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    create_app_user()
