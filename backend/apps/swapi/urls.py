from django.urls import path
from swapi.views import PeopleDownloadAggregateView, PeopleDownloadDetailView, PeopleDownloadListView

urlpatterns = [
    path("", PeopleDownloadListView.as_view(), name="people-download-list"),
    path("<int:pk>/", PeopleDownloadDetailView.as_view(), name="people-download-detail"),
    path("<int:pk>/aggregate/", PeopleDownloadAggregateView.as_view(), name="people-download-aggregate"),
]
