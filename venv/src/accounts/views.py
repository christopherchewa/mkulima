from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.utils import timezone
from django.utils.text import slugify
from django.db.models import Count
from django.template.loader import render_to_string
import json
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.contrib.auth import (
	authenticate, 
	get_user_model, 
	login,
	logout,
	)

from .models import (
	AdminUserProfile, 
	MkulimaUserProfile, 
	CustomerUserProfile,
	Product,
	Order,
	
	)


User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}), max_length=255, required=True, label='')
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}), required=True, label='')

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		
		if username and password:
			user = authenticate(username=username, password=password)
			if not user or not user.is_active:
				raise forms.ValidationError("Sorry invalid login details. Try again")

		return super(UserLoginForm, self).clean(*args, **kwargs)
		
	def login(self, request):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		return user

class UserRegistrationForm(forms.ModelForm):
	first_name =  forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}), label='', required=True)
	last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}), label='', required=True)
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}), label='', required=True)
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email'}), label='', required=True)
	email2 = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Confirm Email'}), label='', required=True)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}), label='', required=True)
	

	class Meta:
		model = User
		fields = ['first_name','last_name','username', 'email', 'email2', 'password']

	def clean_email2(self):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if email != email2:
			raise forms.ValidationError("Emails must match")

		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This email has already been registered")

		return email

class NewSaccoForm(forms.ModelForm):

	class Meta:
		model = AdminUserProfile
		fields = ['sacco_name']

class MkulimaSaccoRegistrationForm(forms.ModelForm):

	class Meta:
		model = MkulimaUserProfile
		fields = ['mkulimaoption']

class SaccoMembersForm(forms.ModelForm):
	first_name = forms.CharField(required=True, label='First Name')
	last_name = forms.CharField(required=True, label='Last Name')
	email = forms.EmailField(required=True, label='Email')
	username = forms.CharField(label='Username')
	
	class Meta:
		model = User
		fields = ['first_name','last_name','email','username']

	def clean_email(self):
		email = self.cleaned_data.get('email')
		email_qs = User.objects.filter(email=email)

		if email_qs.exists():
			raise forms.ValidationError("This email has already been registered")

		return email

class CustomerForm(forms.ModelForm):

	class Meta:
		model = CustomerUserProfile
		fields = ['phonenumber']
#used together with UserReg form


class ProductForm(forms.ModelForm):
	name = forms.CharField(required=True, label='Product Name')
	price = forms.CharField(required=True, label='Product Price')

	class Meta:
		model = Product
		fields = ['name', 'price','description','image','quantity']

class OrderForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'demo-bvd-notempty'
        self.helper.form_class = 'form-horizontal order-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'tap_product'

        self.helper.add_input(Submit('submit', 'Submit'))
        super(OrderForm, self).__init__(*args, **kwargs)

    class Meta:
    	model = Order
    	exclude = ['customer','product','timestamp']




#add views

def login_view(request, template_name="pages-login.html"):
	
	next = request.GET.get("next")

	form = UserLoginForm(request.POST or None)
	if request.POST and form.is_valid():
		user = form.login(request)
		if user:
			login(request, user)
			if next:
				return redirect(next)
			return HttpResponseRedirect('/products/')
	
	return render(request, template_name, {'form':form})


def register_view(request, template_name="add-account.html"):


	return render(request, template_name, {})



def admin_register_view(request, template_name="admin-register.html"):

	

	adminregistrationform = UserRegistrationForm(request.POST or None)

	saccoregistrationform = NewSaccoForm(request.POST or None)

	if adminregistrationform.is_valid() and saccoregistrationform.is_valid():
	

		password = adminregistrationform.cleaned_data.get('password')
		username = adminregistrationform.cleaned_data.get('username')

		sacco_name = saccoregistrationform.cleaned_data.get('sacco_name')

		admin = adminregistrationform.save()
		admin.set_password(password)
		admin.save()

		sacco = saccoregistrationform.save(commit=False)
		sacco.user = admin

		adminobject = User.objects.get(username=username)
		adminobject.groups.add(Group.objects.get(name="Admin"))
		newgroup = Group.objects.create(name=sacco_name)
		adminobject.groups.add(Group.objects.get(name=newgroup.name))


		sacco.save()
		admin = authenticate(username=username, password=password)
		login(request, admin)


		
	return render(request, template_name, {'adminregistrationform': adminregistrationform, 'saccoregistrationform':saccoregistrationform})


def add_sacco_members_view(request, template_name="sacco-member-form.html"):

	admin = request.user

	adminobject = AdminUserProfile.objects.get(user=admin)
	sacco_name = adminobject.sacco_name
	print(sacco_name)


	saccomemberform = MkulimaSaccoRegistrationForm(request.POST or None)
	addsaccomembersform = SaccoMembersForm(request.POST or None)
	

	if addsaccomembersform.is_valid() and saccomemberform.is_valid():
		first_name = addsaccomembersform.cleaned_data.get('first_name')
		last_name = addsaccomembersform.cleaned_data.get('last_name')
		email = addsaccomembersform.cleaned_data.get('email')
		username = addsaccomembersform.cleaned_data.get('username')


		mkulima = addsaccomembersform.save()
		mkulima.set_password(email)

		
		mkulima.save()

		member = saccomemberform.save(commit=False)
		member.user = mkulima

		memberobject = User.objects.get(email=email)
		memberobject.groups.add(Group.objects.get(name=sacco_name))
		memberobject.groups.add(Group.objects.get(name="Mkulima"))
		member.save()

	return render(request, template_name, {'sacco_name':sacco_name, 'addsaccomembersform':addsaccomembersform, 'saccomemberform':saccomemberform})



def add_mkulima_view(request, template_name="mkulima-register.html"):

	
	mkulimaregistrationform = UserRegistrationForm(request.POST or None)

	#will always be none
	addsaccomembersform = MkulimaSaccoRegistrationForm(request.POST or None)

	if mkulimaregistrationform.is_valid():
		mkulima = mkulimaregistrationform.save(commit=False)
		password = mkulimaregistrationform.cleaned_data.get('password')
		username = mkulimaregistrationform.cleaned_data.get('username')
		mkulima = mkulimaregistrationform.save()
		mkulima.set_password(password)
		mkulima.save()
		

		#default sacco value will be None
		member = addsaccomembersform.save(commit=False)
		member.user = mkulima

		memberobject = User.objects.get(username=username)
		memberobject.groups.add(Group.objects.get(name="Mkulima"))
		member.save()
		mkulima = authenticate(username=username, password=password)
		login(request, mkulima)
		
		return redirect('/mkulimapanel/')

	return render(request, template_name, {'mkulimaregistrationform':mkulimaregistrationform, 'addsaccomembersform':addsaccomembersform})


def add_customer_view(request, template_name="customer-register.html"):
	customerregistrationform = UserRegistrationForm(request.POST or None)
	phonenumberregistrationform = CustomerForm(request.POST or None)

	if customerregistrationform.is_valid() and phonenumberregistrationform.is_valid():
		password = customerregistrationform.cleaned_data.get('password')
		username = customerregistrationform.cleaned_data.get('username')

		customer = customerregistrationform.save(commit=False)
		customer.set_password(password)
		customer.save()

		phonenumber = phonenumberregistrationform.save(commit=False)
		phonenumber.user = customer

		customerobject = User.objects.get(username=username)
		customerobject.groups.add(Group.objects.get(name="Customer"))
		phonenumber.save()

		customer = authenticate(username=username, password=password)
		login(request, customer)
		return redirect('/products/')


	return render(request, template_name, {'customerregistrationform':customerregistrationform, 'phonenumberregistrationform':phonenumberregistrationform})



@login_required(login_url='/login/')
def mkulima_panel(request, template_name="mkulima-panel.html"):

	if not request.user.groups.filter(name='Mkulima').exists():
		raise Http404

	

	wakulima = MkulimaUserProfile.objects.all()




	return  render(request, template_name, {'wakulima':wakulima})




@login_required(login_url='/login/')
def add_product_view(request, template_name="add-product.html"):

	

	if not request.user.groups.filter(name='Mkulima').exists():
		raise Http404

	addproductform = ProductForm(request.POST or None, request.FILES or None)

	if addproductform.is_valid():

		product = addproductform.save(commit=False)
		product.user = request.user
		product.save()

		return redirect('/products/editlist/')


	return render(request, template_name, {'addproductform':addproductform})


@login_required(login_url='/login/')
def edit_product_view(request, slug=None, template_name="add-product.html"):

	product = get_object_or_404(Product, slug=slug)
	if request.user != product.user and not request.user.groups.filter(name='Mkulima').exists():
		raise Http404



	product = get_object_or_404(Product, slug=slug)
	addproductform = ProductForm(request.POST or None, request.FILES or None, instance=product)

	if addproductform.is_valid():

		product = addproductform.save(commit=False)

		product.save()
		return redirect('/products/editlist/')


	return render(request, template_name, {'addproductform':addproductform})

@login_required(login_url='/login/')
def delete_product_view(request, slug=None, template_name="product-confirm-delete.html"):

	product = get_object_or_404(Product, slug=slug)
	if request.user != product.user and not request.user.groups.filter(name='Mkulima').exists():
		raise Http404

	

	if request.method == 'POST':
		product.delete()
		return redirect('/products/deletelist/')


	return render(request, template_name, {'product':product})


def product_list_view(request, template_name="index.html"):
	
	today = timezone.now()
	
	saccosobject = Group.objects.order_by('name')
	exclude_id_list = [1,2,3]
	saccos = saccosobject.exclude(id__in=exclude_id_list)
	
	sacco_name = saccos.annotate(Count('user'))



	products_row = Product.objects.order_by('-updated')[:3]
	products_row2 = Product.objects.order_by('-timestamp')[:3]

	mostpopular = Product.objects.order_by('-taps')[:4]
	#topsellers = Product.objects.order_by('taps')[:4]
	newarrivals = Product.objects.order_by('-timestamp')[:4]
	topdeals = Product.objects.order_by('price')[:4]

	topnews1 = Product.objects.order_by('taps')[:3]
	topnews2 = Product.objects.order_by('-timestamp')[:3]

	



	return render(request, template_name, {'today':today, 'products':products_row, 'products2':products_row2, 'mostpopular':mostpopular, 'newarrivals':newarrivals, 'topdeals':topdeals, 'topnews1':topnews1, 'topnews2':topnews2, 'sacco_name':sacco_name})
	

@login_required(login_url='/login/')
def product_editlist(request, template_name="product-editlist.html"):

	if not request.user.groups.filter(name='Mkulima').exists():
		raise Http404

	user = request.user
	products = Product.objects.filter(user=user).order_by('-updated')

	return render(request, template_name, {'products':products})


@login_required(login_url='/login/')
def product_deletelist(request, template_name="product-deletelist.html"):

	if not request.user.groups.filter(name='Mkulima').exists():
		raise Http404
		
	user = request.user
	products = Product.objects.filter(user=user).order_by('-updated')

	return render(request, template_name, {'products':products})

@login_required(login_url='/login/')
def orders_view(request, template_name="orders.html"):

	if not request.user.groups.filter(name='Mkulima').exists():
		raise Http404

	user = request.user
	orders = Order.objects.filter(owner=user).order_by('-timestamp')

	return render(request, template_name, {'orders':orders})



def logout_view(request):
	logout(request)
	return redirect('/login/')




def tap_product(request):
	
	
	today = timezone.now()
	user = request.user
	data = dict()

	product_id = None
	try:
		product_id = request.session['product_id_ref']
		obj = Product.objects.get(id=product_id)
		

	except:
		obj = None
	

	
	if request.method=="POST":
		form = OrderForm(request.POST)
		
		

		if form.is_valid():

			order = form.save(commit=False)
			product = Product.objects.get(id=product_id)
			customer = CustomerUserProfile.objects.get(user=user)
			order.customer = customer
			order.product = product
			order.save()
			data['form_is_valid'] = True
		else:
			data['form_is_valid'] = False


	if request.method=="GET":
		
		product_id = request.GET['product_id']
		
		form = OrderForm()
		data['html_form'] = render_to_string('order-form.html', {'form':form}, request=request)
		taps = 0


		if product_id:
			product = Product.objects.get(id=int(product_id))

			if product:
				taps = product.taps + 1
				product.taps = taps
				product.save()
				data['name'] = product.name
				data['price'] = product.price
				data['description'] = product.description
				
				


	
	

			
	return JsonResponse(data, safe=False)
	


def trash_product(request):
	

	product_id = None
	if request.method=="GET":
		product_id = request.GET['product_id']
		
		

	trashes = 0
	if product_id:
		product = Product.objects.get(id=int(product_id))
		if product:
			
			trashes = product.trashes + 1
			product.trashes = trashes

			product.save()
	

	return HttpResponse(trashes)



