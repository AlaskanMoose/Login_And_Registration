from django.shortcuts import render, redirect
from .models import User
import bcrypt
from django.contrib import messages


def index(request):
	return render(request, 'loginregistration/index.html')
def register(request):
	if request.method == 'POST':
		print "This is request.post on the register button", request.POST
		user = User.userManager.register(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'], request.POST['password_confirm'])
		if 'error' in user:
			print "Not a Valid Registration form"
			return redirect('/')
		if 'theuser' in user:
			print user
			request.session['id'] = user['theuser'][0].id
			print request.session['id']
			print "Valid Registration Form"
			return redirect('/success')	
def login(request):
	if request.method == 'POST':
		print "This is request.post on the login button", request.POST
		user = User.userManager.login(request.POST['email'], request.POST['password'])
		if 'error' in user:
			print "Not a valid email or password"
			return redirect('/')
		if 'theuser' in user:
			request.session['id'] = user['theuser'][0].id
			print "valid email and password combination"
			return redirect('/success')
def success(request):
	users = User.userManager.filter(id = request.session['id'])
	messages.success(request, users[0].first_name+users[0].last_name)
	context = {
		'users': User.userManager.all()
	}
	return render(request, 'loginregistration/success.html', context)
