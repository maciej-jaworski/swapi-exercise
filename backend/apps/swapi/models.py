from django.db import models


class PeopleDownload(models.Model):
    UPLOAD_TO = "people"

    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    downloaded_file = models.FileField(upload_to=UPLOAD_TO)
