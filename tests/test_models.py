# -*- coding: utf-8 -*-
"""
    tests.test_models
    ~~~~~~~~~~~~~~~~~

    tests for data models
"""

import pytest
from sqlalchemy.exc import IntegrityError

from application.models import Status, Submission


@pytest.mark.usefixtures("session")
class TestModels:
    def test_submission_create(self):
        sub1 = Submission().create(**{"title": "title", "email": "email", "card_id": "card_id", "card_url": "card_url"})

        assert Submission().get_by_id(sub1.id)

    def test_submission_delete(self):
        sub1 = Submission().create(**{"title": "title", "email": "email", "card_id": "card_id", "card_url": "card_url"})

        Submission().delete(sub1)
        assert Submission().get_by_id(sub1.id) is None

    def test_submission_title_not_nullable(self):
        with pytest.raises(IntegrityError):
            sub1 = Submission().create(**{"email": "email", "card_id": "card_id", "card_url": "card_url"})

    def test_submission_email_not_nullable(self):
        with pytest.raises(IntegrityError):
            sub1 = Submission().create(**{"title": "title", "card_id": "card_id", "card_url": "card_url"})

    def test_submission_card_id_not_nullable(self):
        with pytest.raises(IntegrityError):
            sub1 = Submission().create(**{"title": "title", "email": "email", "card_url": "card_url"})

    def test_submission_card_url_not_nullable(self):
        with pytest.raises(IntegrityError):
            sub1 = Submission().create(**{"title": "title", "email": "email", "card_id": "card_id"})

    def test_submission_status_default(self):
        sub1 = Submission().create(**{"title": "title", "email": "email", "card_id": "card_id", "card_url": "card_url"})

        assert sub1.status == Status.NEW.value

    def test_base_methods(self):
        # create calls save and new
        sub1 = Submission().create(
            **{
                "title": "title",
                "email": "email",
                "card_id": "card_id",
                "card_url": "card_url",
                "card_email": "card_email",
                "description": "description",
                "notes": "notes",
                "pitch": "pitch",
            }
        )

        assert Submission().get_by_id(sub1.id)
        assert Submission().first(email="email")

        Submission().update(sub1, card_id="new_card_id")
        assert Submission().find(card_id="new_card_id")

        assert Submission().all() is not None
        assert sub1 in Submission().get_all(sub1.id)
        assert Submission().get_or_404(sub1.id) is not None
        assert sub1.to_dict() == {
            "title": sub1.title,
            "card_id": sub1.card_id,
            "card_url": sub1.card_url,
            "created_at": sub1.created_at,
            "updated_at": sub1.updated_at,
            "type": "Submission",
            "email": sub1.email,
            "hook": sub1.hook,
            "status": sub1.status,
            "card_email": sub1.card_email,
            "description": sub1.description,
            "notes": sub1.notes,
            "pitch": sub1.pitch,
        }

        with pytest.raises(ValueError):
            sub1._isinstance(str())

        Submission().delete(sub1)
        assert Submission().get_by_id(sub1.id) is None

    def test_status_new(self):
        status = Status.NEW
        assert status.value is 1

    def test_status_inreview(self):
        status = Status.INREVIEW
        assert status.value is 2

    def test_status_scheduled(self):
        status = Status.SCHEDULED
        assert status.value is 3

    def test_status_archived(self):
        status = Status.ARCHIVED
        assert status.value is 4


# flake8: noqa
