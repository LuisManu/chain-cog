from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	website = models.CharField(max_length=130, blank=True, null=True)
	location = models.CharField(max_length=100, blank=True, null=True)
	about = models.CharField(max_length=200, blank=True, null=True)
	picture = models.ImageField(upload_to='profile_images', blank=True, null=True)
	ip_address = models.CharField(max_length=120)

	def __unicode__(self):
		return self.user.username


class Category(models.Model):
	name = models.CharField(max_length=128, unique=True)
	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)
	
	class Meta:
		verbose_name_plural = 'Categories'

	def __unicode__(self):
		return self.name


class Bicycle(models.Model):
	user = models.ForeignKey(User)
	category = models.ForeignKey(Category)
	views = models.IntegerField(default=0)
	year = models.IntegerField(blank=True, null=True)
	brand = models.CharField(max_length=128)
	model_type = models.CharField(max_length=128)
	frame_fork = models.CharField(max_length=128, blank=True,  null=True)
	shifters = models.CharField(max_length=128, blank=True, null=True)
	derailleurs = models.CharField(max_length=128, blank=True, null=True)
	crankset_bb = models.CharField(max_length=128, blank=True, null=True)
	cog_or_cassette = models.CharField(max_length=128, blank=True, null=True)
	chain = models.CharField(max_length=128, blank=True, null=True)
	pedals = models.CharField(max_length=128, blank=True, null=True)
	brakes_levers = models.CharField(max_length=128, blank=True, null=True)
	headset = models.CharField(max_length=128, blank=True, null=True)
	hubs = models.CharField(max_length=128, blank=True, null=True)
	rims = models.CharField(max_length=128, blank=True, null=True)
	handlebars_stem = models.CharField(max_length=128, blank=True, null=True)
	saddle_seatpost = models.CharField(max_length=128, blank=True, null=True)
	tires = models.CharField(max_length=128, blank=True, null=True)
	main_image = models.ImageField(upload_to='bicycle_images')
	image1 = models.ImageField(upload_to='bicycle_images', blank=True, null=True)
	image2 = models.ImageField(upload_to='bicycle_images', blank=True, null=True)
	image3 = models.ImageField(upload_to='bicycle_images', blank=True, null=True)
	image4 = models.ImageField(upload_to='bicycle_images', blank=True, null=True)
	summary = models.TextField(blank=True, null=True)
	slug = models.SlugField(unique=True)
	date_time = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		brandModel = self.brand + str(self.id)
		self.slug = slugify(brandModel)
		super(Bicycle, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('dashboard')

	def __unicode__(self):
		return self.brand
