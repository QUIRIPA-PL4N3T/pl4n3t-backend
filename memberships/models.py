from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _


class Membership(models.Model):
    FREE = 'FREE'
    BASIC = 'BASIC'
    PREMIUM = 'PREMIUM'
    VIP = 'VIP'

    MEMBERSHIP_CHOICES = [
        (FREE, _('Free')),
        (BASIC, _('Básica')),
        (PREMIUM, _('Premium')),
        (VIP, _('VIP')),
    ]
    name = models.CharField(_('Nombre'), max_length=255)
    membership_type = models.CharField(
        _('Tipo de Membresía'),
        max_length=50,
        choices=MEMBERSHIP_CHOICES,
        default=FREE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text=_('Duración en días'), default=365)
    description = models.TextField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class CompanyMembership(models.Model):
    company = models.OneToOneField(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='membership',
        null=True,
        blank=True,
    )
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return f'{self.company.name} - {self.membership.name}'
