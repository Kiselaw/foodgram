import django_filters

from api.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name='author_id',
                                       lookup_expr='exact')
    tags = django_filters.CharFilter(field_name='tags__slug',
                                     lookup_expr='exact',
                                     method='my_tags_filter')

    class Meta:
        model = Recipe
        fields = ['author', 'tags']

    def my_tags_filter(self, queryset, name, value):
        query_params = self.request.query_params
        tags_query = query_params.getlist('tags')
        return queryset.filter(tags__slug__in=tags_query).distinct()
