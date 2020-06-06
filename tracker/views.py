from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView
from .models import Country, Total, Name
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import render
from .resources import CountryResource
from django.http import HttpResponse
from import_export import resources
import subprocess
import requests
import json
import pyttsx3
import speech_recognition as sr
import re
import threading
import time

import os




API_KEY = 'txGsgA6p2w46'
PROJECT_TOKEN = 't3GeyApmVs_c'
RUN_TOKEN = 'tz24XhGQ6_cK'


class Data:
	def __init__(self, api_key, project_token):
		self.api_key = api_key
		self.project_token = project_token
		self.params = {
			"api_key": self.api_key
		}
		self.data = self.get_data()

	def get_data(self):
		response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params=self.params)
		data = json.loads(response.text)
		return data

	def get_total_cases(self):
		data = self.data['total']

		for content in data:
			if content['name'] == "Coronavirus Cases:":
				return content['total_cases']
		return 0

	def get_total_deaths(self):
		data = self.data['total']

		for content in data:
			if content['name'] == "Deaths:":
				return content['total_deaths']

		return 0

	def get_total_recovered(self):
		data = self.data['total']

		for content in data:
			if content['name'] == "Recovered:":
				return content['total_recovered']

		return 0

	def get_country_data(self, country):
		data = self.data["country"]

		for content in data:
			if content['name'].lower() == country.lower():
				return content

		return "0"

	def get_all_country_data(self):
		data = self.data["country"]

		return data


	def get_list_of_countries(self):
		countries = []
		for country in self.data['country']:
			countries.append(country['name'].lower())

		return countries

	def update_data(self):
		response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run', params=self.params)

		def poll():
			time.sleep(0.1)
			old_data = self.data
			while True:
				new_data = self.get_data()
				if new_data != old_data:
					self.data = new_data
					print("Data updated")
					break
				time.sleep(5)


		t = threading.Thread(target=poll)
		t.start()

def speak(text):
	engine = pyttsx3.init()
	engine.say(text)
	engine.runAndWait()


def get_audio():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		audio = r.listen(source)
		said = ""

		try:
			said = r.recognize_google(audio)
		except Exception as e:
			print("Exception:", str(e))

	return said.lower()






def handle(name):
	c=0
	data = Data(API_KEY, PROJECT_TOKEN)
	END_PHRASE = "stop"
	country_list = data.get_list_of_countries()

	TOTAL_PATTERNS = {
					re.compile(r"[\w\s]+ total [\w\s]+ cases"):data.get_total_cases,
					re.compile(r"[\w\s]+ total cases"):data.get_total_cases,
                	re.compile(r"[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
                	re.compile(r"[\w\s]+ total deaths"): data.get_total_deaths,
                    re.compile(r"[\w\s]+ total [\w\s]+ recovered"): data.get_total_recovered,
                    re.compile(r"[\w\s]+ total recovered"): data.get_total_recovered,
					}

	COUNTRY_PATTERNS = {
					re.compile(r"[\w\s]+ cases [\w\s]+"): lambda country: data.get_country_data(country).get('cases', '0'),
            	    re.compile(r"[\w\s]+ deaths [\w\s]+"): lambda country: data.get_country_data(country).get('deaths', '0'),
            	    re.compile(r"[\w\s]+ recovered [\w\s]+"): lambda country: data.get_country_data(country).get('recovered', '0'),
            	    re.compile(r"[\w\s]+ tests [\w\s]+"): lambda country: data.get_country_data(country).get('tests', '0'),
					}

	UPDATE_COMMAND = "update"

	while True:
		if(c==0):
			speak('Hi '+ name)
			speak("I am here to provide you with information related to COVID 19. Speak exit to end the session.")
			c+=1
		speak("Listening")
		text = get_audio()
		print(text)
		result = None

		for pattern, func in COUNTRY_PATTERNS.items():
			if pattern.match(text):
				words = set(text.split(" "))
				for country in country_list:
					if country in words:
						result = func(country)
						break

		for pattern, func in TOTAL_PATTERNS.items():
			if pattern.match(text):
				result = func()
				break

		if text == UPDATE_COMMAND:
			result = "Data is being updated. This may take a moment!"
			data.update_data()

		if result:
			speak(result)
			print(result)

		if text.find(END_PHRASE) != -1:
			speak("Thank you for interacting with me. Have a good day. Byeee.")
			break





class VoiceView(CreateView):
	template_name = 'voice.html'
	model = Name
	fields = {'name',}
	def submit(request):
		if request.method == 'POST':
			name = request.POST['name']
			handle(str(name))


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



class GraphView(TemplateView):
	template_name = 'graph_temp.html'


class TrackView(ListView):
	model = Country
	template_name = 'track.html'
	login_url = 'login'
	paginate_by = 5
	ordering = ['name']

class HomePageView(ListView):
	template_name = 'index.html'
	model = Total


class TrackDetailView(DetailView):
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
