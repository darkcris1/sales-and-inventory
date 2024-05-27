import django_filters
from .models import Sale
from django.db.models import Q

class SaleFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='transaction_date', lookup_expr='gte', label='Start Date')
    end_date = django_filters.DateFilter(field_name='transaction_date', lookup_expr='lte', label='End Date')
    search = django_filters.CharFilter(method='filter_by_all', label='Search')

    class Meta:
        model = Sale
        fields = ['start_date', 'end_date', 'search', 'item', 'transaction_date', 'profile']

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(item__name__icontains=value)
        )