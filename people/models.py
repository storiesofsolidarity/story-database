from django.db import models
from django.contrib.auth.models import User


class UserManager(models.Manager):
    def get_or_create_user(self, **kwargs):
        user__name = kwargs.pop('user__name')

        try:
            first_name, last_name = user__name.split(' ')  # simple but stupid
            # TODO, improve name parsing
        except ValueError:
            first_name = ""
            last_name = user__name

        user, new_user = User.objects.get_or_create(first_name=first_name, last_name=last_name)
        if new_user:
            if first_name:
                user.username = ("{}_{}".format(user.first_name, user.last_name)).lower()
            else:
                user.username = last_name
            user.save()

        kwargs['user'] = user
        return super(UserManager, self).get_or_create(**kwargs)


class AbstractUserBase(models.Model):
    user = models.OneToOneField(User)
    objects = UserManager()

    class Meta:
        abstract = True


class Author(AbstractUserBase):
    occupation = models.CharField(max_length=100, null=True, blank=True)
    employer = models.CharField(max_length=100, null=True, blank=True)

    photo = models.ImageField(blank=True, null=True, upload_to="author_photo")
    sms_number = models.CharField(blank=True, null=True, max_length=15)

    employed = models.BooleanField(default=True)
    part_time = models.BooleanField(default=False)

    anonymous = models.BooleanField(default=False, help_text=
                                    "Group account like 'Web Anonymous' or 'SMS Anonymous'")

    def __unicode__(self):
        if self.occupation and self.employer:
            return "{}, {}, {}".format(self.user, self.occupation, self.company)
        elif self.user:
            return self.user.__unicode__()
        else:
            return "Unnamed Author"


class Organizer(AbstractUserBase):
    organization = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    # city, state, zip
    # website
