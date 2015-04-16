from django.apps import AppConfig
from actstream import registry


class PeopleConfig(AppConfig):
    name = 'people'

    def read(self):
        registry.register(self.get_model('Author'))
        registry.register(self.get_model('Organizer'))
        import people.signals
