import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class CommentFilter(django_filters.FilterSet):
	impact = CharFilter(field_name='impact', lookup_expr='icontains')
	start_date = DateFilter(field_name="date", lookup_expr='gte')
	end_date = DateFilter(field_name="date", lookup_expr='lte')


	class Meta:
		model = Comment
		fields = ['satellite', 'transponder','complaint_type','active']
		# fields = '__all__'
		# exclude = ['customer', 'date_created']