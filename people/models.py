from django.db import models
from django.contrib.auth.models import User


class AnonymousUserManager(models.Manager):
    def next_anonymous(self):
        """ If a name isn't provided, find the next Anonymous #N """
        first_name = "Anonymous"
        last_anon = User.objects.filter(first_name=first_name).count()
        last_name = "#%d" % (last_anon+1,)
        return (first_name, last_name)

    def get_or_create_user(self, **kwargs):
        """ Get_or_create user by name, creating anonymous if necessary """
        user__name = kwargs.pop('user__name')
        is_anonymous = False

        if user__name:
            try:
                first_name, last_name = user__name.split(' ', 1)  # simple but stupid
                # TODO, improve name parsing
            except (ValueError, AttributeError):
                # can't split, make first_name blank and last_name as provided
                first_name, last_name = "", user__name
        else:
            # None or blank, make it anonymous
            first_name, last_name = self.next_anonymous()
            is_anonymous = True

        if first_name:
            username = ("{}_{}".format(first_name, last_name)).lower()
        else:
            username = last_name

        user, new_user = User.objects.get_or_create(first_name=first_name, last_name=last_name, username=username)
        if new_user:
            user.anonymous = is_anonymous
            user.save()

        kwargs['user'] = user
        return super(AnonymousUserManager, self).get_or_create(**kwargs)


class AbstractUserBase(models.Model):
    user = models.OneToOneField(User)
    objects = AnonymousUserManager()

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
