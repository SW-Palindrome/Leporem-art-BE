from functools import reduce
from operator import or_

import django_filters
from django.db.models import Case, F, Q, Value, When


class OrderingFilter(django_filters.OrderingFilter):
    def get_ordering_value(self, param):
        field_name = self.param_map.get(param, param)
        return field_name

    def filter(self, qs, value):
        if not value:
            return qs
        field_name = self.get_ordering_value(value[0])
        qs = qs.annotate(is_sold=Case(When(current_amount=0, then=Value(None)), default=Value(1)))
        return qs.order_by(F('is_sold').asc(nulls_last=True), field_name)


class PriceRangeFilter(django_filters.RangeFilter):
    def filter(self, qs, value):
        qs = qs.annotate(is_sold=Case(When(current_amount=0, then=Value(None)), default=Value(1)))
        return super().filter(qs, value).order_by(F('is_sold').asc(nulls_last=True), '-display_dt')


class ItemFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(ItemFilter, self).__init__(*args, **kwargs)

        if 'nickname' not in self.data:
            super().queryset.annotate(is_sold=Case(When(current_amount=0, then=Value(None)), default=Value(1)))

    price = PriceRangeFilter()
    category = django_filters.CharFilter(method='category_filter')
    nickname = django_filters.CharFilter()
    search = django_filters.CharFilter(method='search_filter')
    ordering = OrderingFilter(
        fields=(('-display_dt', 'recent'), ('-like_count', 'likes'), ('-price', 'price_high'), ('price', 'price_low'))
    )

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
