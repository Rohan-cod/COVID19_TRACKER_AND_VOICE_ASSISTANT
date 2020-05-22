

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






def handle():
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
		print("Listening...")
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
			print("Exit")
			break


handle()



