from django.http import HttpResponse

import apps.es


def create(request):
    aggregate = apps.es.es_app.create_aggregate(a=5)
    apps.es.es_app.run()
    return HttpResponse(f"Hallo {aggregate.id} - {aggregate.a}")
