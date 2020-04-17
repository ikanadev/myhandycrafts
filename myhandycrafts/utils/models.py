""" Django models utilities."""

# Django
from django.db import models


class MyHandycraftsModel(models.Model):
    """My Handycrafts base Model.

    MyHandycrafts Model is an abstract base class from which every
    other model in the project will insert in their code. This clas provides
    every tables with the following attributes:
        - is_deleted (Boolean): Store if the object is deleted
        - created_at (DateTime): Store the datetime the objects was created.
        - updated_at (DateTime): Store the last datetime the object was updated.
        - deleted_at (DateTime): Store the datetime the objects was deleted.
    """
    is_deleted = models.BooleanField(
        'is_deleted',
        default=False,
        help_text='show when the object is active.'
    )

    created_at = models.DateTimeField(
        'create_at',
        auto_now_add=True,
        help_text='Date time on which the objects was created.'
    )

    updated_at = models.DateTimeField(
        'updated_at',
        auto_now=True,
        help_text='Date time on which the objects was last updated.'
    )

    deleted_at = models.DateTimeField(
        'updated_at',
        auto_now=True,
        help_text='Date time on which the objects was deleted.'
    )

    created_by = models.PositiveIntegerField(
        null=True,
        help_text='created_by'
    )

    updated_by = models.PositiveIntegerField(
        null=True,
        help_text='updated_by'
    )

    deleted_by = models.PositiveIntegerField(
        null=True,
        help_text='deleted_by'
    )

    class Meta:
        """Meta Option."""
        abstract = True
        get_latest_by = 'created_at'
        ordering = ['-created_at', '-updated_at']
