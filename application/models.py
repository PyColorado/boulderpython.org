# -*- coding: utf-8 -*-
"""
    models.py
    ~~~~~~~~~
    application data models
"""

from enum import Enum
from datetime import datetime as dt

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr

from application.extensions import db


class Base(db.Model):
    """Convenience base DB model class. Extends `db.Model`

    Helper class to inherit in database models that adds a set of helpful methods
    and automation steps like conventional table names, primary keys, and utility
    columns for created and updated timestamps.
    """

    @declared_attr
    def __tablename__(self):
        return "{}".format(self.__name__.lower())

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: dt.utcnow(), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: dt.utcnow(), onupdate=lambda: dt.utcnow(), nullable=False)

    def _isinstance(self, model, raise_error=True):
        """Checks if the specified model instance matches the base's model.

        By default this method will raise a `ValueError` if the model is not the
        expected type.

        Args:
            model: the model instance to check
            raise_error: flag to raise an error on a mismatch

        Returns:
            rv: returned if model is an instance of the class

        """
        rv = isinstance(model, self.__class__)
        if not rv and raise_error:
            raise ValueError("%s is not of type %s" % (model, self.__class__))
        return rv

    def _preprocess_params(self, kwargs):
        """Returns a preprocessed dictionary of parameters. Used by default
        before creating a new instance or updating an existing instance.

        :param kwargs: a dictionary of parameters
        """
        kwargs.pop("csrf_token", None)
        return kwargs

    def save(self, model):
        """Commits the model to the database and returns the model

        :param model: the model to save
        """
        self._isinstance(model)
        db.session.add(model)
        db.session.commit()
        return model

    def update(self, model, **kwargs):
        """Returns an updated instance of the base model class.

        :param model: the model to update
        :param ``**kwargs``: update parameters
        """
        self._isinstance(model)
        for k, v in self._preprocess_params(kwargs).items():
            setattr(model, k, v)
        db.session.commit()
        return model

    def all(self):
        """Returns a generator containing all instances of the base model."""
        return self.__class__.query.all()

    def get_by_id(self, id):
        """Returns an instance of the base model with the specified id. Returns `None` if an
        instance with the specified id does not exist.

        :param id: the instance id
        """
        return self.__class__.query.get(id)

    def get_all(self, *ids):
        """Returns a list of instances of the base model with the specified ids.

        :param `*ids`: instance ids
        """
        return self.__class__.query.filter(self.__class__.id.in_(ids)).all()

    def find(self, **kwargs):
        """Returns a list of instances of the base model filtered by the specified key word arguments.

        :param ``**kwargs``: filter parameters
        """
        return self.__class__.query.filter_by(**kwargs)

    def first(self, **kwargs):
        """Returns the first instance found of the base model filtered by the specified
        key word arguments.

        :param ``**kwargs``: filter parameters
        """
        return self.find(**kwargs).first()

    def get_or_404(self, id):
        """Returns an instance of the base model with the specified id or raises an 404 error
        if an instance with the specified id does not exist.

        :param id: the instance id
        """
        return self.__class__.query.get_or_404(id)

    def new(self, **kwargs):
        """Returns a new, unsaved instance of the base model class.

        :param ``**kwargs``: instance parameters
        """
        return self.__class__(**self._preprocess_params(kwargs))

    def create(self, **kwargs):
        """Returns a new, saved instance of the base model class.

        :param ``**kwargs``: instance parameters
        """
        return self.save(self.new(**kwargs))

    def delete(self, model):
        """Immediately deletes the specified model instance.

        :param model: the model instance to delete
        """
        self._isinstance(model)
        db.session.delete(model)
        db.session.commit()

    def to_dict(self, *args, **kwargs):
        """returns a dict of all model attributes.
        excludes primary_key and foreign_keys

        :param d: an empty dictionary
        """
        d = dict(
            (c.name, getattr(self, c.name)) for c in self.__table__.columns if not c.primary_key and not c.foreign_keys
        )
        d["type"] = self.__class__.__name__
        return d


class Status(Enum):
    """Status class, extends `enum`. Simple enumerable of submission statuses.

    Attributes:
        NEW (int): submission status is new
        INREVIEW (int): submission status is in-review
        SCHEDULED (int): submission status is scheduled
        ARCHIVED (int): submission status is archived
    """

    NEW = 1
    INREVIEW = 2
    SCHEDULED = 3
    ARCHIVED = 4


class Submission(Base):
    """Submission class

    Stores a talk submission and it's Trello card's identifiers

    Attributes:
        email    (str): email of the submitter
        card_id  (str): the Trello Card ID
        card_url (str): the Trello Card URL
        status   (int): the submission status, Int maps to the Status enum class.
        hook     (str): the ID for the Trello Card's webhook

    Todo:
        * Should store name of talk, though if we change on Trello it should update via webhook
    """

    title = Column(db.String(255), nullable=False)
    description = Column(db.String(4096), nullable=True)
    pitch = Column(db.String(4096), nullable=True)
    notes = Column(db.String(4096), nullable=True)
    email = Column(db.String(255), nullable=False)
    card_id = Column(db.String(255), nullable=False, unique=True)
    card_url = Column(db.String(255), nullable=False, unique=True)
    status = Column(db.Integer, nullable=False, default=Status.NEW.value)
    hook = Column(db.String(255))
    card_email = Column(db.String(255))


class TrelloList(Base):
    """Trello List class

    Maps a trello list by symbolic name to its ID on this particular Trello board

    Attributes:
        email    (str): email of the submitter
        card_id  (str): the Trello Card ID
        card_url (str): the Trello Card URL
        status   (int): the submission status, Int maps to the Status enum class.
        hook     (str): the ID for the Trello Card's webhook

    Todo:
        * Should store name of talk, though if we change on Trello it should update via webhook
    """

    list_symbolic_name = Column(db.String(255), nullable=False, unique=True)
    list_id = Column(db.String(255), nullable=False, unique=True)
