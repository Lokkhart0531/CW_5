from pathlib import Path

from cw_5.config import settings
from cw_5.db.managers.pg_db_manager import PostgresDBManager


def create_database():
    """
    Создается БД, которую мы указывем
    :rtype: object
    :return:
    """
    db_manager = PostgresDBManager(db_name='postgres')
    db_manager.connect()
    db_manager.connection.autocommit = True

    try:
        with db_manager.connection.cursor() as cursor:
            cursor.execute(f'drop database if exists {settings.DB_NAME}')
            cursor.execute(f'create database {settings.DB_NAME}')

        db_manager.commit()

    finally:
        db_manager.disconnect()


def apply_migrations():
    db_manager = PostgresDBManager
    db_manager.connect()

    try:
        with db_manager.connection.cursor() as cursor:
            for migration in sorted(settings.MIGRATIONS_DIR.glob('*.sql')):
                cursor.execute(_read_migrations(migration))

            db_manager.commit()
    finally:
        db_manager.disconnect()


def _read_migrations(file_path: Path) -> str:
    """
    Функция для миграции, конкретно чтение
    :param file_path:
    :return:
    """
    with file_path.open(encoding='utf-8') as f:
        return f.read()


