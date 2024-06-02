import datetime as dt

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime

from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Basis(DeclarativeBase):
    pass


class User(Basis):
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(50), nullable=False)
    created_on = Column(DateTime(), default=dt.datetime.now)

    def __str__(self):
        return f"<{self.id}> {self.first_name} {self.last_name} aka {self.username}"

    def __repr__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


engine = create_engine("sqlite:///My Database/users.db?echo=True")

Basis.metadata.create_all(engine)

factory = sessionmaker(bind=engine)
