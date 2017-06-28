from __future__ import unicode_literals
import re, datetime, bcrypt
from django.contrib.auth import authenticate
from dateutil.relativedelta import *
from datetime import *
from dateutil.relativedelta import relativedelta
from django.db import models
from dateutil.parser import parse as parse_date
from django.utils.timezone import get_fixed_timezone, utc

class UserManager(models.Manager):
	def register(self, data):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

		errors = []

		for field in data:
			if len(data[field]) == 0:
				errors.append(field.replace('_', ' ').title() + " may not be empty")
		if len(data['first_name']) < 2 or len(data['last_name']) < 2:
			errors.append("First Name and Last Name must be at least 2 characters long")

		if not data['first_name'].isalpha() or not data['last_name'].isalpha():
			errors.append("First Name and Last Name may only be letters")

		if not EMAIL_REGEX.match(data['email']):
			errors.append("Email not valid")

		if len(data['password']) < 8:
			errors.append("Password must be at least 8 characters long")

		if data['password'] != data['confirm_password']:
			errors.append("Passwords do not match")

		try:
			User.objects.get(email=data['email'])
			errors.append("Email already registered. Forgot your password?")
		except:
			pass

		#user needs to be at least 13 to enter the site
		try:
			birthdate = datetime.datetime.strptime(data['birthday'], '%Y-%m-%d')
			today = datetime.datetime.today()
			age = relativedelta(today, birthdate)
			if age.years < 13:
				errors.append("You are too young to create an account")
		except:
			pass


		if len(errors) == 0:
			hashed_pw = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
			print(hashed_pw)

			user = User.objects.create(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=hashed_pw, birthday=data['birthday'])
			return user

		return errors

	def login(self, data):
		try:
			user = User.objects.get(email=data['email'])
			if bcrypt.hashpw(data['password'].encode(), user.password.encode()) == user.password.encode():
				return user

			return "Your Password is incorrect"

		except:
			return "Email not registered in system"


class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password= models.CharField(max_length=255)
	birthday = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

class TripManager(models.Manager):
    def add_trip(self, request):
        errors = self.trip_validations(request)

        if errors:
            return errors

        user = User.objects.get(id=request.session['user']['user_id'])

        Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], planner=user)

        return errors

    def join_trip(self, request, id):
        user = User.objects.get(id=request.session['user']['user_id'])

        trip = Trip.objects.get(id=id)

        trip.travelers.add(user)

    def trip_validations(self, request):
        errors = []

        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        if start_date:
            start_date = parse_date(start_date).date()
            if start_date < date.today():
                errors.append('Start date must be today or in the future.')
        else:
            errors.append('Please add a start date.')

        if end_date:
            end_date = parse_date(end_date).date()
            if end_date < date.today():
                errors.append('End date must be today or in the future.')
        else:
            errors.append('Please add an end date.')

        if start_date and end_date:
            if start_date > end_date:
                errors.append('End date must be after or the same as start date.')

        if not request.POST['destination']:
            errors.append('Please add a destination.')
        if not request.POST['description']:
            errors.append('Please add a description.')

        return errors

class Trip(models.Model):
    destination = models.CharField(max_length = 50)
    description = models.CharField(max_length = 140)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    planner = models.ForeignKey(User, related_name='trip')
    travelers = models.ManyToManyField(User, related_name='trips')

    objects = TripManager()
