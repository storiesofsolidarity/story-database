from django.apps import AppConfig
from actstream import registry

class SoSConfig(AppConfig):
    name = 'sos'

    def ready(self):
        registry.register(self.get_model('Author'))
        registry.register(self.get_model('Organizer'))
