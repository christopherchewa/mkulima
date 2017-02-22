from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.urlresolvers import reverse
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField



def profile_upload_location(instance, filename):

	return "%s/%s/%s" %(str(instance.usertype), str(instance.user.username),  filename)

def product_upload_location(instance, filename):

	products_folder = "Products"

	return "%s/%s/%s" %(products_folder, str(instance.user.username), filename)


# Create your models here.


class AdminUserProfile(models.Model):
	user = models.OneToOneField(User)
	sacco_name = models.CharField(max_length=255, null=False, blank=False, unique=True)
	image = models.ImageField(null=True, blank=True, upload_to=profile_upload_location, width_field='width_field', height_field='height_field')
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	#usertype - only for pic upload purposes and some if statements in some views
	usertype = models.CharField(max_length=255, default="Admin")
	#
	location = models.CharField(max_length=255, blank=True, null=True)
	website = models.URLField(blank=True, null=True)
	bio = models.TextField(blank=True, null=True)
	
	
	def __str__(self):
		return self.user.username



class MkulimaUserProfile(models.Model):
	user = models.OneToOneField(User)
	sacco_name = models.CharField(max_length=255, default="None")
	MKULIMA_OPTIONS = (

			('Goods', 'Goods'),
			('Services', 'Services'),
			('Both', 'Both'),

		)

	mkulimaoption = models.CharField(max_length=30, choices=MKULIMA_OPTIONS, null=False, blank=False, default="Goods")
	image = models.ImageField(null=True, blank=True, upload_to=profile_upload_location, width_field='width_field', height_field='height_field')
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	usertype = models.CharField(max_length=255, default="Mkulima")
	location = models.CharField(max_length=255, blank=True, null=True)
	website = models.URLField(blank=True, null=True)	
	bio = models.TextField(blank=True, null=True)
	phonenumber = models.CharField(max_length=10, default="0701555677")

	
	


	def __str__(self):
		return self.user.username
	

class CustomerUserProfile(models.Model):
	user = models.OneToOneField(User)
	image = models.ImageField(null=True, blank=True, upload_to=profile_upload_location, width_field='width_field', height_field='height_field')
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	phonenumber = models.CharField(max_length=10)
	usertype = models.CharField(max_length=255, default="Customer")




	def __str__(self):
		return self.user.username


class Product(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=255, null=False, blank=False)
	price = models.IntegerField(default=0)
	description = models.TextField(null=True, blank=True)
	slug = models.SlugField(unique=True)
	taps = models.IntegerField(default=0)
	trashes = models.IntegerField(default=0)
	image = models.ImageField(null=True, blank=True, upload_to=product_upload_location, width_field='width_field', height_field='height_field')
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	timestamp = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now = True, auto_now_add = False)
	quantity = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(1000), MinValueValidator(1)])

	
	def __str__(self):
		return self.name


class Order(models.Model):
	customer = models.ForeignKey(User, related_name='customer')
	product = models.ForeignKey(Product)
	owner = models.ForeignKey(User, related_name='owner')
	quantity = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(1000), MinValueValidator(1)])
	timestamp = models.DateTimeField(default=timezone.now)
	cleared = models.BooleanField(default=False)
	

	def __str__(self):
		return self.product.name



def create_slug(instance, new_slug=None):


	#new_slug is none
	slug = slugify(instance.name)

	#new_slug exists
	if new_slug is not None:
		slug = new_slug
	qs = Product.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()

	if exists:
		new_slug = " %s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)

	return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)



pre_save.connect(pre_save_post_receiver, sender=Product)