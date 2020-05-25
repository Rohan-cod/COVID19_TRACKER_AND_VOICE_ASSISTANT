from django.db import models

# Create your models here.
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

class Country(models.Model):
	name = models.CharField(max_length=120)
	cases = models.CharField(max_length=120)
	deaths = models.CharField(max_length=120)
	recovered = models.CharField(max_length=120)
	tests = models.CharField(max_length=120)

	def __str__(self):
		return self.name


	def get_absolute_url(self):
		return reverse('track_detail', args=[str(self.id)])

class Total(models.Model):
	total_cases = models.CharField(max_length=120)
	total_deaths = models.CharField(max_length=120)
	total_recovered = models.CharField(max_length=120)

	def __str__(self):
		return str(self.total_cases)


class Name(models.Model):
	name = models.CharField(max_length=120)

	def __str__(self):
		return str(self.name)