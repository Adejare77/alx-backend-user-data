#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB():
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """returns a user object/instance """
        # DB is not a table, thus using "self" refers to DB() instance
        # and not User instance. Thus, create a User instance
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ returns first row found in the the users table """
        try:
            find_first_user = \
                self._session.query(User).filter_by(**kwargs).first()
        except InvalidRequestError as e:
            raise InvalidRequestError

        if not find_first_user:
            raise NoResultFound

        return find_first_user

    def update_user(self, user_id: int, **kwargs: dict) -> None:
        """ update an existing user """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise NoResultFound
        for key, value in kwargs.items():
            if key in user.__dict__:
                setattr(user, key, value)
            else:
                raise ValueError
        self._session.commit()
