from django.contrib import admin
from swapi.models import PeopleDownload


@admin.register(PeopleDownload)
class PeopleDownloadAdmin(admin.ModelAdmin):
    list_display = (
        "created_timestamp",
        "downloaded_file",
    )
