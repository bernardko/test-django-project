import shortuuid

from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import ShortUUIDField

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import pre_save

class UserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)

class User(AbstractUser):
    """
    User Model for dumpdata / loaddata
    
    Natural Keys are implemented with a namespaced shortuuid as 
    the primary key which will allow us to accurately use dumpdata and 
    loaddata on the command line to dump/load user data to and from a 
    json file.
    """
    id = ShortUUIDField(primary_key=True, editable=False)

    objects = UserManager()

    def __str__(self):
        return "%s" % self.username
    
    def natural_key(self):
        return (self.username,)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = shortuuid.uuid(name="%s" % self.natural_key())
        super().save(*args, **kwargs)

# Needed so that loaddata will create the shortuuid before saving the model
@receiver(pre_save)
def create_shortuuid(sender, instance, *args, **kwargs):
    if sender == User and not instance.id:
        instance.id = shortuuid.uuid(name="%s" % instance.natural_key())