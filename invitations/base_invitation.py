from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .managers import BaseInvitationManager


@python_2_unicode_compatible
class AbstractBaseInvitation(models.Model):
    key = models.CharField(verbose_name=_('key'), max_length=64, unique=True)
    inviter = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    approved_at = models.DateTimeField(verbose_name=_('approved at'),
        blank=True, null=True)
    accepted_at = models.DateTimeField(verbose_name=_('accepted at'),
        blank=True, null=True)
    sent_at = models.DateTimeField(verbose_name=_('sent at'), null=True,
        default=timezone.now)


    objects = BaseInvitationManager()

    class Meta:
        abstract = True

    @classmethod
    def create(cls, email, inviter=None, **kwargs):
        raise NotImplementedError(
            'You should implement the create method class'
        )

    def key_expired(self):
        raise NotImplementedError(
            'You should implement the key_expired method'
        )

    def send_invitation(self, request, **kwargs):
        raise NotImplementedError(
            'You should implement the send_invitation method'
        )

    def __str__(self):
        raise NotImplementedError(
            'You should implement the __str__ method'
        )
