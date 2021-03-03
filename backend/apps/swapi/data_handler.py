from typing import List

import petl
from swapi.api_client import RelatedResourceAttributeRetriever

FIELDS_TO_REMOVE = [
    "films",
    "species",
    "vehicles",
    "starships",
    "created",
    "edited",
]


def load_list_to_petl_table(object_list: List[dict]):
    return petl.io.json.fromdicts(object_list)


def perform_people_table_transformations(petl_table: petl.Table) -> petl.Table:
    # Add a date column (%Y-%m-%d) based on edited date
    new_table = petl.addfield(
        petl_table,
        "date",
        lambda row: row["edited"][:10],  # Seems more efficient than parsing and formatting back to isoformat
    )

    # Resolve the homeworld field into the homeworld's name (/planets/1/ -> Tatooine)
    homeworld_name_retriever = RelatedResourceAttributeRetriever("name")
    new_table = petl.convert(new_table, "homeworld", lambda v: homeworld_name_retriever.fetch_from_url(v))

    # Fields referencing different resources and date fields other than date/birth_year can be dropped
    return petl.transform.basics.cutout(new_table, *FIELDS_TO_REMOVE)
