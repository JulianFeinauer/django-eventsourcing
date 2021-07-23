from django.db import models


class ProjectionRecord(models.Model):
    id = models.UUIDField(primary_key=True, null=False, editable=False)

    a = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.id} - {self.a}"
