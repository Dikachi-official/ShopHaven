# TO ADD FILTER FEATURE TO OUR API
from API.models import Product
from django_filters.rest_framework import FilterSet


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'id': ['exact'],
            'price': ['gt', 'lt']
        }
