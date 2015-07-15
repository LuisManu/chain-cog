from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from .models import Category, Bicycle, UserProfile
from .forms import CategoryForm, BicycleForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User
from .search import get_query
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.core.cache import cache


def get_ip(request):
	try:
		x_forward = request.META.get("HTTP_X_X_FORWARDED_FOR")
		if x_forward:
			ip = x_forward.split(",")[0]
		else:
			ip = request.META.get("REMOTE_ADDR")
	except:
		ip = ""
	return ip


def index(request):
	category_list = Category.objects.all()
	bicycle_list = Bicycle.objects.order_by('-date_time')[:8]
	context_dict = {'categories': category_list, 'bicycles': bicycle_list}
	return render(request, 'bike/index.html', context_dict)
	

def about(request):
	return render(request, 'bike/about.html', {})


def category(request, category_name_slug):
	context_dict = {}
	context_dict['result_list'] = None
	context_dict['query'] = None
	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			result_list = run_query(query)
			context_dict['result_list'] = result_list
			context_dict['query'] = query
	try:
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name
		bicycles = Bicycle.objects.filter(category=category).order_by('-views')
		context_dict['bicycles'] = bicycles
		context_dict['category'] = category
		all_cat_names = Category.objects.all()
		context_dict['cat_names'] = all_cat_names
	except Category.DoesNotExist:
		pass
	if not context_dict['query']:
		context_dict['query'] = category.name
	return render(request, 'bike/category.html', context_dict)


def add_bicycle(request):
	if request.method == 'POST':
		form = BicycleForm(request.POST, request.FILES)
		if form.is_valid():
			bicycle = form.save(commit=False)
			bicycle.views = 0
			bicycle.user = User.objects.get(username=request.user)
			bicycle.save()
			return index(request)
		else:
			print form.errors
	else:
		form = BicycleForm()
	context_dict = {'form': form}
	return render(request, 'bike/add_bicycle.html', context_dict)


def search(request):
    query_string = ''
    found_entries = None
    cat = Category.objects.all()
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, [
        	'year', 'brand', 'model_type',
        	'summary', 'frame_fork', 'tires',
        	'shifters', 'derailleurs', 'crankset_bb',
        	'cog_or_cassette', 'chain', 'pedals',
        	'brakes_levers', 'headset', 'hubs',
        	'rims', 'handlebars_stem', 'saddle_seatpost'
        	
        	])
        found_entries = Bicycle.objects.filter(entry_query)
    return render(request, 'bike/search.html',
                          {'query_string': query_string, 'found_entries': found_entries, 'cat': cat})


def profile(request, user_name):
	context_dict = {}
	try:
		user = User.objects.get(username=user_name)
		userprofile = UserProfile.objects.get(user=user)
		bicycles = Bicycle.objects.filter(user=user)
		context_dict = {'bicycles': bicycles, 'user': user, 'userprofile': userprofile}
	except User.DoesNotExist:
		user = None
	return render(request, 'bike/profile.html', context_dict)


@login_required
def dashboard(request):
	context_dict = {}
	try:
		user = User.objects.get(username=request.user.username)
		bicycles = Bicycle.objects.filter(user=user)
		context_dict = {'bicycles': bicycles, 'user': user}
	except User.DoesNotExist:
		user = None
	return render(request, 'bike/dashboard.html', context_dict)


def bicycle(request, brand_model):
	context_dict ={}
	try:
		bicycle = Bicycle.objects.get(slug=brand_model)
		user = bicycle.user
		allbicycles = Bicycle.objects.filter(user=user)
		bicycle.views = bicycle.views + 1
		bicycle.save()
		context_dict = {'bicycle': bicycle, 'allbicycles': allbicycles}
	except Bicycle.DoesNotExist:
		bicycle = None
	return render(request, 'bike/bicycle.html', context_dict)


def add_profile(request):
	registered = False
	if request.method == 'POST':
		profile_form = UserProfileForm(request.POST, request.FILES)
		if profile_form.is_valid():
			profile = profile_form.save(commit=False)
			profile.user = User.objects.get(username=request.user)
			profile.ip_address = get_ip(request)
			profile.save()
			registered = True
		else:
			print user_form.errors, profile_form.errors
	else:
		profile_form = UserProfileForm()
	return render(request, 'bike/add_profile.html',
		{ 'profile_form': profile_form, 'registered': registered})


def areyousure(request, slug):
	bici = Bicycle.objects.get(slug=slug)
	return render(request, 'bike/are_you_sure.html', {'bici': bici})


def delete(request, slug):
	to_delete = Bicycle.objects.get(slug=slug)
	to_delete.delete()
	return HttpResponse("Your bike was deleted. :(")