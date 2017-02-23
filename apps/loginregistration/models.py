from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from django.contrib import messages

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
NAME_REGEX = re.compile(r'(^[a-zA-Z])')
class UserManager(models.Manager):
	def register(self, first_name, last_name, email, password, password_confirm):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.password = password
		self.password_confirm = password_confirm
		errors = []

		if len(self.first_name) < 3:
			errors.append("Must be atleast 2 characters first_name")
		if len(self.last_name) < 3:
			errors.append("Must be atleast 2 characters last_name")
		if not NAME_REGEX.match(self.first_name):
			errors.append("First Name must be all characeters")
		if not NAME_REGEX.match(self.last_name):
			errors.append("Last Name must be all characters")
		if not EMAIL_REGEX.match(self.email):
			errors.append("Not a Valid Email Format")

		emails = User.userManager.filter(email=self.email)
		if len(emails) > 0:
			errors.append("Email already exists")

		if len(self.password) < 8:
			errors.append("Password must be atleast 8 characeters long")
		if not self.password == self.password_confirm:
			errors.append("Passwords must match")

		print errors
		if errors:
			return {'error': errors}
		else:
			hashed = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())
			User.userManager.create(first_name=self.first_name, last_name=self.last_name, email=self.email, password=hashed)
			return {'theuser': User.userManager.filter(email=self.email)}

	def login(self, email, password):
		self.email = email
		self.password = password 
		errors = []
		users = User.userManager.filter(email= self.email)
		if len(users) > 0:
			if bcrypt.hashpw(self.password.encode(), users[0].password.encode()) == users[0].password:
				return {'theuser': users}
			else:
				return {"error": "The password and email does not match"}
		else:
			return {"error": "This email does not exist"}
		
class User(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=1000)
	userManager = UserManager()
		


