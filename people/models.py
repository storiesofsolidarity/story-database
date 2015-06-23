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
        user__name = kwargs.pop('user__name', None)
        first_name = kwargs.pop('first_name', None)
        last_name = kwargs.pop('last_name', None)
        email = kwargs.pop('email', '')
        is_anonymous = False

        if first_name and last_name:
            pass
        elif user__name:
            try:
                first_name, last_name = user__name.split(' ', 1)  # simple but stupid
                first_name = first_name.strip()
                last_name = last_name.strip()
                # TODO, improve name parsing
            except (ValueError, AttributeError):
                # can't split, make first_name blank and last_name as provided
                first_name, last_name = "", user__name
        elif email:
            # use email address before domain
            last_name, domain = email.split('@', 1)
            first_name = ""
        else:
            # None or blank, make it anonymous
            first_name, last_name = self.next_anonymous()
            is_anonymous = True

        if first_name:
            first_last = u"{}_{}".format(first_name.replace(' ', '_'), last_name.replace(' ', '_'))
            username = first_last.lower()
        else:
            username = last_name.lower()

        username = username.replace('__', '_').replace('.', '')

        user, new_user = User.objects.get_or_create(username=username)
        if new_user:
            user.first_name = first_name
            user.last_name = last_name
            user.anonymous = is_anonymous
            user.email = email
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
            return "{}, {}, {}".format(self.user, self.occupation, self.employer)
        elif self.user:
            return self.user.__unicode__()
        else:
            return "Unnamed Author"


class Organizer(AbstractUserBase):
    organization = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    # city, state, zip
    # website
