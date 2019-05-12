import dateutil.parser as datetime_parser
import pytz
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from . import models
from . import serializers


class ViewSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ApiAccountViewSet(viewsets.ModelViewSet):
    queryset = models.AccountToTrack.objects.all()
    serializer_class = serializers.AccountSerializer
    pagination_class = ViewSetPagination


class ApiTransactionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.TransactionETH.objects.all()
    serializer_class = serializers.TransactionETHSerializer
    pagination_class = ViewSetPagination

    def get_queryset(self):
        query = models.TransactionETH.objects.all()

        filter_kwargs = dict()

        for k, v in self.request.query_params.items():
            if k in ["fromAddress", "toAddress"]:
                filter_kwargs[f'{k}'] = v
                continue
            if k in ["fromDate", "toDate"]:
                # this is naive filter. We need to check validity of time. and return
                # some specific response for incorrect params
                timestamp = datetime_parser.parse(v).replace(tzinfo=pytz.UTC).timestamp()
                if k == "fromDate":
                    filter_kwargs['timestamp__gte'] = timestamp
                    continue
                if k == "toDate":
                    filter_kwargs['timestamp__lte'] = timestamp
                    continue

        if len(filter_kwargs.keys()):
            query = query.filter(**filter_kwargs)

        return query.order_by('timestamp')


def redirect_to_api(request):
    return redirect("/api")
