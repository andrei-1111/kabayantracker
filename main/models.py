

from django.db import models
from django.utils.translation import ugettext_lazy as _

STATUS_FOUND = 'found'
STATUS_CHOICES = (
	(STATUS_FOUND, 'FOUND'),
)

class Person(models.Model):
    full_name = models.CharField(_('Full Name'), max_length=200, blank=True, null=True)
    address = models.CharField(_('Address'), max_length=200, blank=True, null=True)
    age = models.CharField(_('Age'), max_length=200, blank=True, null=True)
    gender = models.CharField(_('Gender'), max_length=200, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default=STATUS_FOUND)

    def __unicode__(self):

        return "{0} - {1} - {2}".format(self.full_name, self.address, self.status)
