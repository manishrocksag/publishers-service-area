from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


class LanguageTypes(object):
    US_EN = 0
    EN = 1


class CurrencyTypes(object):
    USD = 0


LANGUAGE_CHOICES = (
    (LanguageTypes.US_EN, _('us_en')),
    (LanguageTypes.EN, _("en")),
)

CURRENCY_CHOICES = (
    (CurrencyTypes.USD, _("usd")), )


@python_2_unicode_compatible
class Publisher(models.Model):
    """
    """

    publisher_id = models.CharField(_('user_id'), max_length=254, unique=True)
    name = models.CharField(_('first name'), max_length=254)
    email = models.EmailField(max_length=70, blank=True, null= True, unique= True)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    language = models.IntegerField(choices=LANGUAGE_CHOICES, default=0)
    currency = models.IntegerField(choices=CURRENCY_CHOICES, default=0)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this publisher should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))

    class Meta:
        verbose_name = _('publisher')
        verbose_name_plural = _('publishers')

    def __str__(self):
        return self.publisher_id
