from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from foodgram_backend.settings import REGEX_USER


def validate_username(value):
    """
    Метод проверки username на корректность.
    regex=^[\w.@+-]+\z.
    """
    if not REGEX_USER.match(value):
        raise ValidationError(
            _('%(value)s is invalid username!'),
            params={'value': value},
        )
    return value
