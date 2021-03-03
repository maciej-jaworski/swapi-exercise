import os
import uuid
from pathlib import Path

import petl
from django.conf import settings
from swapi.api_client import StarWarsAPIClient
from swapi.data_handler import load_list_to_petl_table, perform_people_table_transformations
from swapi.models import PeopleDownload

# ensure uploads directory exists
UPLOAD_DIR = os.path.join(settings.MEDIA_ROOT, PeopleDownload.UPLOAD_TO)
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


def download_new_snapshot():
    results = StarWarsAPIClient.get_full_list_of("people")
    table: petl.Table = perform_people_table_transformations(load_list_to_petl_table(results))

    file_path = os.path.join(UPLOAD_DIR, f"{str(uuid.uuid4())}.csv")

    petl.tocsv(table, file_path)

    snapshot = PeopleDownload(downloaded_file=file_path)
    snapshot.save()
    return snapshot
