import os

import petl
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView
from swapi.downloader import download_new_snapshot
from swapi.models import PeopleDownload


class PeopleDownloadListView(ListView):
    queryset = PeopleDownload.objects.all().order_by("-created_timestamp")
    template_name = "swapi/download_list.html"

    def post(self, request):
        download_new_snapshot()
        return redirect("people-download-list", permanent=False)


class PeopleDownloadDetailView(DetailView):
    count_increment = 10
    count_query_kwarg = "show"

    object: PeopleDownload
    model = PeopleDownload
    template_name = "swapi/people.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filename"] = self.object.downloaded_file.name.split(os.path.sep)[-1]
        context["count_query_kwarg"] = self.count_query_kwarg

        table = petl.fromcsv(self.object.downloaded_file)
        context["header"] = petl.header(table)

        try:
            record_count_to_show = int(self.request.GET.get(self.count_query_kwarg))
        except (TypeError, ValueError):
            record_count_to_show = self.count_increment

        # Potentially expensive, count could be cached / saved per dataset
        if petl.nrows(table) > record_count_to_show:
            context[
                "load_more_url"
            ] = f"{self.request.path}?{self.count_query_kwarg}={record_count_to_show+self.count_increment}"

        context["rows"] = petl.records(petl.head(table, record_count_to_show))

        return context


class PeopleDownloadAggregateView(DetailView):
    columns_query_kwarg = "columns"

    object: PeopleDownload
    model = PeopleDownload
    template_name = "swapi/aggregate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filename"] = self.object.downloaded_file.name.split(os.path.sep)[-1]
        context["columns_query_kwarg"] = self.columns_query_kwarg
        table = petl.fromcsv(self.object.downloaded_file)

        full_table_header = list(petl.header(table))
        context["column_options"] = full_table_header

        selected_columns = [c for c in self.request.GET.getlist(self.columns_query_kwarg) if c in full_table_header]
        context["selected_columns"] = selected_columns

        if selected_columns:
            context["header"] = selected_columns + ["Count"]
            context["rows"] = petl.records(
                petl.aggregate(table, selected_columns[0] if len(selected_columns) == 1 else selected_columns, len)
            )

        return context
