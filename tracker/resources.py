from import_export import resources
from import_export.fields import Field
from .models import Country

class CountryResource(resources.ModelResource):
	class Meta:
		model = Country
		fields = ['name','cases','deaths','recovered','tests']