from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse

def profile_upload_location(instance, filename):

	return "%s/%s/%s" %(str(instance.usertype), str(instance.user.username),  filename)

def product_upload_location(instance, filename):

	products_folder = "Products"

	return "%s/%s/%s" %(products_folder, str(instance.user.username), filename)


# Create your models here.

class UserType(models.Model):
	usertype = models.CharField(max_length=120)

	def __str__(self):
		return self.usertype



class AdminUserProfile(models.Model):
	user = models.OneToOneField(User)
	sacco_name = models.CharField(max_length=255, null=False, blank=False)
	image = models.ImageField(null=True, blank=True, upload_to=profile_upload_location, width_field='width_field', height_field='height_field')
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	usertype = models.CharField(max_length=120, default="Admin")
	isadmin = models.BooleanField(default=True)
	ismkulima = models.BooleanField(default=False)
	iscustomer = models.BooleanField(default=False)
	


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
	usertype = models.CharField(max_length=120, default="Mkulima")
	isadmin = models.BooleanField(default=False)
	ismkulima = models.BooleanField(default=True)
	iscustomer = models.BooleanField(default=False)


	def __str__(self):
		return self.user.username
	

class CustomerUserProfile(models.Model):
	user = models.OneToOneField(User)
	bio = models.TextField(null=True, blank=True)
	image = models.ImageField(null=True, blank=True, upload_to=profile_upload_location, width_field='width_field', height_field='height_field')
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	usertype = models.CharField(max_length=120, default="Customer")
	isadmin = models.BooleanField(default=False)
	ismkulima = models.BooleanField(default=False)
	iscustomer = models.BooleanField(default=True)
	

	def __str__(self):
		return self.user.username


class Product(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=255, null=True, blank=True)
	price = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)
	quantity = models.IntegerField(default=0)
	taps = models.IntegerField(default=0)
	trashes = models.IntegerField(default=0)
	image = models.ImageField(null=True, blank=True, upload_to=product_upload_location, width_field='width_field', height_field='height_field')
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)

	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('product-details', kwargs={'slug':self.slug})

class Order(models.Model):
	user = models.ForeignKey(User, default=1)
	product = models.ForeignKey(Product)
	owner = models.ForeignKey(User, related_name='owner', default=1)
	timestamp = models.DateTimeField(auto_now_add=False, auto_now=False)

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