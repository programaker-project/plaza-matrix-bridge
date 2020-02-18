from sqlalchemy import Column, Integer, String, MetaData, Column, ForeignKey, UniqueConstraint, Table

metadata = MetaData()

MatrixUsers = Table(
    'MATRIX_USERS', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('matrix_user_id', String(256)))

PlazaUsers = Table(
    'PLAZA_USERS', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('plaza_user_id', String(36), unique=True))

PlazaUsersInMatrix = Table(
    'PLAZA_USERS_IN_MATRIX', metadata,
    Column('plaza_id', Integer, ForeignKey('PLAZA_USERS.id'), primary_key=True),
    Column('matrix_id', Integer, ForeignKey('MATRIX_USERS.id'), primary_key=True),
    __table_args__=(UniqueConstraint('plaza_id', 'matrix_id')))
