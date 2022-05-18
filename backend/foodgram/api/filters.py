import django_filters

from api.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name='name',
                                       lookup_expr='icontains')
    tags = django_filters.CharFilter(field_name='tags__name',
                                     lookup_expr='exact',
                                     method='my_tags_filter')

    class Meta:
        model = Recipe
        fields = ['author', 'name']

    def my_tags_filter(self, queryset, name, value):
        query_params = self.request.query_params
        # print(query_params)
        tags_query = query_params.getlist('tags')
        # print(tags_query)
        # print(value)
        # tags = Tag.objects.filter(name__in=tags_query)
        return queryset.filter(tags__name__in=tags_query)
