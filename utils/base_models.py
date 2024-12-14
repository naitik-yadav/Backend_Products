from django.db import models
from django.utils.translation import gettext_lazy as _


class CreatedUpdatedOnMixin(models.Model):
    """
        Model Mixin for created_at and updated_at
    """
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Creation At"))
    updated_at = models.DateTimeField(auto_now=True, help_text=_("Updated At"))

    class Meta:
        abstract = True
        ordering = ["-id"]


class RequestResponseMixin(models.Model):
    """
        Model Mixin for request_json, response_json
        and response_status ...
    """
    request_json = models.JSONField(null=True, blank=True)
    response_json = models.JSONField(null=True, blank=True)
    request_status = models.CharField(max_length=3, blank=True)

    class Meta:
        abstract = True