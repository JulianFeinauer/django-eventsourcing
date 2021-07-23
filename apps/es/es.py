from typing import Union

from eventsourcing.application.decorators import applicationpolicy
from eventsourcing.application.django import DjangoApplication
from eventsourcing.application.process import ProcessApplication
from eventsourcing.domain.model.aggregate import AggregateRoot
from eventsourcing.domain.model.decorators import attribute



print("Hello!!!")


class CustomAggregate(AggregateRoot):
    def __init__(self, a, **kwargs):
        super(CustomAggregate, self).__init__(**kwargs)
        self._a = a

    @attribute
    def a(self):
        """Mutable attribute a."""


class MyApplication(DjangoApplication, ProcessApplication):
    persist_event_type = AggregateRoot.Event

    @applicationpolicy
    def policy(self, repository, event):
        """Do nothing by default"""

    @policy.register(AggregateRoot.Created)
    def _(self, repository, event):
        print(f"Event: {event}")
        from apps.es.models import ProjectionRecord
        projection_record = ProjectionRecord(id=event.originator_id, a=event.a)
        print(f"Record: {projection_record}")
        repository.save_orm_obj(projection_record)

    @policy.register(AggregateRoot.AttributeChanged)
    def _(self, repository, event):
        print(f"Event: {event}")
        from apps.es.models import ProjectionRecord
        projection_record = ProjectionRecord.objects.get(pk=event.originator_id)
        setattr(projection_record, event.name[1:], event.value)
        print(f"Record: {projection_record}")
        repository.save_orm_obj(projection_record)

    def create_aggregate(self, a):
        agg = CustomAggregate.__create__(a=1)
        agg.__save__()
        agg.a = a
        agg.__save__()
        return agg


application: Union[MyApplication, None] = None
