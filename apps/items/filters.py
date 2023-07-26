from functools import reduce
from operator import or_

import django_filters
from django.db.models import Q


class ItemFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        fields=(
            ('-display_dt', 'recent'),
            ('-like_count', 'likes'),
            ('price', 'price_low'),
            ('-price', 'price_high'),
        )
    )
    price = django_filters.RangeFilter()
    category = django_filters.CharFilter(method='category_filter')
    nickname = django_filters.CharFilter()
    search = django_filters.CharFilter(method='search_filter')

    def category_filter(self, queryset, name, value):
        queryset = queryset.filter(category_mappings__category__category__in=value.split(','))
        return queryset

    def search_filter(self, queryset, name, value):
        search_fields = ('nickname', 'title', 'description')
        queries = [Q(**{f'{field}__icontains': value}) for field in search_fields]
        if queryset:
            combined_query = reduce(or_, queries)
            queryset = queryset.filter(combined_query)
        return queryset

    class Meta:
        fields = ('ordering', 'price', 'nickname', 'category', 'search')

    def __init__(self, *args, **kwargs):
        super(ItemFilter, self).__init__(*args, **kwargs)
