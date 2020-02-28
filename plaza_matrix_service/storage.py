import re
import os
from xdg import XDG_DATA_HOME

import sqlalchemy

from . import models

DB_PATH_ENV = 'PLAZA_MATRIX_BRIDGE_DB_PATH'

if os.getenv(DB_PATH_ENV, None) is None:
    _DATA_DIRECTORY = os.path.join(XDG_DATA_HOME, "plaza", "bridges", "matrix")
    CONNECTION_STRING = "sqlite:///{}".format(os.path.join(_DATA_DIRECTORY, 'db.sqlite3'))
else:
    CONNECTION_STRING = os.getenv(DB_PATH_ENV)


class EngineContext:
    def __init__(self, engine):
        self.engine = engine
        self.connection = None

    def __enter__(self):
        self.connection = self.engine.connect()
        return self.connection

    def __exit__(self, exc_type, exc_value, tb):
        self.connection.close()

class StorageEngine:
    def __init__(self, engine):
        self.engine = engine

    def _connect_db(self):
        return EngineContext(self.engine)

    def register_user(self, matrix_user, plaza_user):
        with self._connect_db() as conn:
            matrix_id = self._get_or_add_matrix_user(conn, matrix_user)
            plaza_id = self._get_or_add_plaza_user(conn, plaza_user)

            check = conn.execute(
                sqlalchemy.select([models.PlazaUsersInMatrix.c.plaza_id])
                .where(
                    sqlalchemy.and_(
                        models.PlazaUsersInMatrix.c.plaza_id == plaza_id,
                        models.PlazaUsersInMatrix.c.matrix_id == matrix_id))
            ).fetchone()

            if check is not None:
                return

            insert = models.PlazaUsersInMatrix.insert().values(plaza_id=plaza_id,
                                                               matrix_id=matrix_id)
            conn.execute(insert)

    def get_matrix_users(self, plaza_user):
        with self._connect_db() as conn:
            plaza_id = self._get_or_add_plaza_user(conn, plaza_user)
            join = sqlalchemy.join(models.MatrixUsers, models.PlazaUsersInMatrix,
                                   models.MatrixUsers.c.id
                                   == models.PlazaUsersInMatrix.c.matrix_id)

            results = conn.execute(
                sqlalchemy.select([
                    models.MatrixUsers.c.matrix_user_id,
                ])
                .select_from(join)
                .where(models.PlazaUsersInMatrix.c.plaza_id == plaza_id)
            ).fetchall()

            return [
                row[0]
                for row in results
            ]

    def is_matrix_user_registered(self, user_id):
        with self._connect_db() as conn:
            result = conn.execute(
                sqlalchemy.select([
                    models.MatrixUsers.c.id,
                ])
                .where(models.MatrixUsers.c.matrix_user_id == user_id)
            ).fetchone()
            return result is not None

    def get_plaza_users_from_matrix(self, user_id):
        with self._connect_db() as conn:
            join = (sqlalchemy.join(models.PlazaUsers, models.PlazaUsersInMatrix,
                                    models.PlazaUsers.c.id
                                    == models.PlazaUsersInMatrix.c.plaza_id)
                    .join(models.MatrixUsers,
                          models.PlazaUsersInMatrix.c.matrix_id == models.MatrixUsers.c.id))

            results = conn.execute(
                sqlalchemy.select([
                    models.PlazaUsers.c.plaza_user_id,
                ])
                .select_from(join)
                .where(models.MatrixUsers.c.matrix_user_id == user_id)
            ).fetchall()

            return map(lambda result: result.plaza_user_id, results)

    def _get_or_add_matrix_user(self, conn, matrix_user):
        check = conn.execute(
            sqlalchemy.select([models.MatrixUsers.c.id])
            .where(models.MatrixUsers.c.matrix_user_id == matrix_user)
        ).fetchone()

        if check is not None:
            return check.id

        insert = models.MatrixUsers.insert().values(matrix_user_id=matrix_user)
        result = conn.execute(insert)
        return result.inserted_primary_key[0]

    def _get_or_add_plaza_user(self, conn, plaza_user):
        check = conn.execute(
            sqlalchemy.select([models.PlazaUsers.c.id])
            .where(models.PlazaUsers.c.plaza_user_id == plaza_user)
        ).fetchone()

        if check is not None:
            return check.id

        insert = models.PlazaUsers.insert().values(plaza_user_id=plaza_user)
        result = conn.execute(insert)
        return result.inserted_primary_key[0]


def get_engine():
    # Create path to SQLite file, if its needed.
    if CONNECTION_STRING.startswith('sqlite'):
        db_file = re.sub("sqlite.*:///", "", CONNECTION_STRING)
        os.makedirs(os.path.dirname(db_file), exist_ok=True)

    engine = sqlalchemy.create_engine(CONNECTION_STRING, echo=True)
    metadata = models.metadata
    metadata.create_all(engine)

    return StorageEngine(engine)
