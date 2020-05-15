import requests
import json
import pyttsx3
import speech_recognition as sr
import re
import threading
import time

import os

from django.core.management.base import BaseCommand
from tracker.models import Country, Total

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



class Command(BaseCommand):
	help = "collect data"
	def handle(self, *args, **options):
		data = Data(API_KEY, PROJECT_TOKEN)
		total_cases = data.get_total_cases()
		total_deaths = data.get_total_deaths()
		total_recovered = data.get_total_recovered()

		Total.objects.update_or_create(
			total_cases=total_cases,
			total_deaths=total_deaths,
			total_recovered=total_recovered
			)

		all_countries_data = data.get_all_country_data()

		for country in all_countries_data:
			name=country.get('name',"")
			cases=country.get('cases',0)
			deaths=country.get('deaths',0)
			recovered=country.get('recovered',0)
			tests=country.get('tests',0)

			Country.objects.update_or_create(
				name=name,
				cases=cases,
				deaths=deaths,
				recovered=recovered,
				tests=tests
			)

		print("Success")
