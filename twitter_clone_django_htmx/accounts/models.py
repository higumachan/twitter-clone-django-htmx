import logging
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

logger = logging.getLogger(__name__)


class CustomUser(AbstractUser):

    @property
    def email_domain(self):
        domain = self.email.split('@')[-1]  # NAME@DOMAIN.COM -> [ 'NAME', 'DOMAIN.COM']
        return domain

    @property
    def display_name(self):
        return f'{self.last_name}, {self.first_name} ({self.username})'
