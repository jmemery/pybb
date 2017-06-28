from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import User


def index(request):
	return render(request, 'pythonapp/index.html')


def register(request):
	result = User.objects.register(request.POST)

	if isinstance(result, list):
		for err in result:
			messages.add_message(request, messages.ERROR, err)
		return redirect('/')

	request.session['id'] = result.id
	request.session['name'] = result.first_name

	return redirect('/success')

def login(request):
	result = User.objects.login(request.POST)

	if isinstance(result, str):
		messages.add_message(request, messages.ERROR, result)
		return redirect('/')

	request.session['id'] = result.id
	request.session['name'] = result.first_name

	return redirect('/success')

def print_errors(request, error_list):
    for error in error_list:
        messages.add_message(request, messages.ERROR, error)

def success(request):
	if not 'id' in request.session:
		return redirect('/')
	return render(request, 'pythonapp/success.html')
def session_check(request):
    if 'user' in request.session:
        return True
    else:
        return False
def logout(request):
	request.session.clear()
	return redirect('/')
def main(request):

    #context = {
    #    'users_trips': Trip.objects.filter(planner__id=request.session['name']['user_id']),
    #    'joined_trips': Trip.objects.filter(travelers__id=request.session['name']['user_id']),
    #    'all_trips': Trip.objects.all()
    #    }
    return render(request, 'pythonapp/main.html')
def planner(request):
    if session_check(request):
        return render(request, 'pythonapp/plan.html')
    return redirect('/')
def show(request, id):
    if session_check(request):
        context = {
            'trip': Trip.objects.get(id=id),
            'attendees': User.objects.filter(trips__id=id)
        }
        return render(request, 'pythonapp/show.html', context)
	return redirect('/')
def jointr(request, id):
    if session_check(request):
        Trip.objects.join_trip(request, id)
    return redirect('pythonapp:show', id)
def addnew(request):
	if session_check(request):
		errors = Trip.objects.addnew(request)
		if errors:
			print errors(request, errors)
		else:
			return redirect('pythonapp/plan.html')
	return redirect('/')
def others(request):
	user = request.session['user.name']
	context = {
	    'users_trips': Trip.objects.filter(planner=request.session['user']),
	    'joined_trips': Trip.objects.filter(traveler=request.session['user']),
	    'all_trips': Trip.objects.all()
	    }
#        context = {
#            'users_trips': Trip.objects.filter(planner__id=request.session['user']['user_id']),
#            'joined_trips': Trip.objects.filter(travelers__id=request.session['user']['user_id']),
#            'all_trips': Trip.objects.all()
#        }
    	return render(request, 'pythonapp/others.html', context)
