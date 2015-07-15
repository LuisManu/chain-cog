from django import forms
from django.contrib.auth.models import User
from .models import Bicycle, Category, UserProfile
from django.views.generic.edit import UpdateView
from datetime import datetime


class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Please enter the category name.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Category
		fields = ('name',)


class BicycleForm(forms.ModelForm):
	summary = forms.CharField(label='Summary', widget=forms.Textarea(attrs={'placeholder': 'Love your bike? A few words about the ride.'}), required=False)

	class Meta:
		model = Bicycle
		fields = (
			'category', 'year', 'brand', 
			'model_type', 'frame_fork', 'shifters',
			'derailleurs', 'crankset_bb', 'cog_or_cassette',
			'chain', 'pedals', 'brakes_levers',
			'headset', 'hubs', 'rims',
			'handlebars_stem', 'saddle_seatpost', 'tires',
			'summary', 'main_image', 'image1',
			'image2', 'image3', 'image4',
			)
	
		exclude = ['user', 'date_time']


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['location', 'about', 'website', 'picture']


class BicycleUpdate(UpdateView):
    model = Bicycle
    fields = ['year', 'brand', 'model_type',
        	'frame_fork', 'tires',
        	'shifters', 'derailleurs', 'crankset_bb',
        	'cog_or_cassette', 'chain', 'pedals',
        	'brakes_levers', 'headset', 'hubs',
        	'rims', 'handlebars_stem', 'saddle_seatpost',
        	'main_image', 'image1',  'image2',
        	'image3',  'image4', 'summary'
        	]
    template_name = 'bike/bicycle_update_form.html'


class UserUpdate(UpdateView):
	model = User
	fields = ['username', 'email']
	template_name = 'bike/update_user.html'

	def get_object(self, queryset=None):
		return self.request.user
