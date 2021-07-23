import os

from django.apps import AppConfig
from django.core.exceptions import AppRegistryNotReady
from eventsourcing.application.notificationlog import NotificationLogReader

import apps.es
from apps.es.es import MyApplication


class EsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.es'

    def ready(self):
        try:
            if os.environ.get('RUN_MAIN', None) != "true":
                return
            print("We are ready now!")

            apps.es.es_app = MyApplication()
            # Follow itself
            apps.es.es_app.follow(apps.es.es_app.name, apps.es.es_app.notification_log)

            aggregate = apps.es.es_app.create_aggregate(a=1)
            aggregate.a = 2
            aggregate.__save__()

            print(aggregate)

            print("----------")
            print("This is all stored events:")
            print("----------")

            reader = NotificationLogReader(apps.es.es_app.notification_log)

            for event_notification in reader.read():
                print(event_notification)

            print(reader.position)
        except AppRegistryNotReady:
            pass

