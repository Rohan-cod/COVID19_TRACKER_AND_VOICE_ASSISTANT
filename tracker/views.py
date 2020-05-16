from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, DetailView
from .models import Country, Total
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import render
from .resources import CountryResource
from django.http import HttpResponse
from import_export import resources

def export_csv(request):
    country_resource = CountryResource()
    countries = country_resource.export()
    response = HttpResponse(countries.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="countries.xls"'
    return response

def export_json(request):
    country_resource = CountryResource()
    countries = country_resource.export()
    response = HttpResponse(countries.json, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="countries.json"'
    return response



class GraphView(LoginRequiredMixin, TemplateView):
	template_name = 'graph.html'


class TrackView(LoginRequiredMixin, ListView):
	model = Country
	template_name = 'track.html'
	login_url = 'login'
	paginate_by = 5
	ordering = ['name']

class HomePageView(ListView):
	template_name = 'index.html'
	model = Total


class VoiceView(TemplateView):
	template_name = 'voice.php'


class TrackDetailView(LoginRequiredMixin, DetailView):
	model = Country
	template_name = 'track_detail.html'
	login_url = 'login'

def search_view(request):
	ctx = {}
	url_parameter = request.GET.get("q")

	if url_parameter:
		countries = Country.objects.filter(name__icontains=url_parameter)
	else:
		countries = Country.objects.all()

	ctx["countries"] = countries

	if request.is_ajax():
		html = render_to_string(
			template_name="track-results-partial.html", 
			context={"countries": countries}
		)

		data_dict = {"html_from_view": html}

		return JsonResponse(data=data_dict, safe=False)

	return render(request, "track_search.html", context=ctx)
