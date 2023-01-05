from django_filters import rest_framework as filters
from .models import JobOffer, EXPERIENCE, FORM_OF_EMPLOYMENT, OPERATING_MODE, WORKING_TIME, TAGS


class JobOfferFilter(filters.FilterSet):
    """
    The function accepts fields and indicates how job offers can be filtered
    """

    tags = filters.ChoiceFilter(choices=TAGS)
    min_price = filters.NumberFilter(field_name="salary_from", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="salary_up_to", lookup_expr='lte')
    experience = filters.ChoiceFilter(choices=EXPERIENCE)
    form_of_employment = filters.ChoiceFilter(choices=FORM_OF_EMPLOYMENT)
    operationg_mode = filters.ChoiceFilter(choices=OPERATING_MODE)
    location = filters.CharFilter(field_name="cities", lookup_expr='name__icontains')
    working_time = filters.ChoiceFilter(choices=WORKING_TIME)

    class Meta:
        model = JobOffer
        fields = [
            'tags',
            'salary_from',
            'salary_up_to',
            'experience',
            'form_of_employment',
            'operationg_mode',
            'cities',
            'working_time'
        ]
