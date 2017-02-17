from django.conf.urls import url
from . import views

# Create your models here.

urlpatterns = [

	url(r'^products/$', views.product_list_view, name='product-list'),
	
	#ajax
	url(r'^products/details/$', views.product_details_view, name = 'product-details'),

	
	url(r'^products/tap_product/$', views.tap_product, name='tap_product'),
	url(r'^products/trash_product/$', views.trash_product, name='trash_product'),
	


	
	url(r'^mkulimapanel/$', views.mkulima_panel, name = 'mkulima-panel'),
	url(r'^orders/$', views.orders_view, name='orders'),

	

	#Mkulima Panel
	url(r'^products/create/$', views.add_product_view, name = 'product-create'),
	url(r'^products/editlist/$', views.product_editlist, name='product-editlist'),
	url(r'^products/deletelist/$', views.product_deletelist, name='product-deletelist'),





	
 	url(r'^products/(?P<slug>[\w-]+)/edit/$', views.edit_product_view, name = 'product-edit'),
 	url(r'^products/(?P<slug>[\w-]+)/delete/$', views.delete_product_view, name = 'product-delete'),
 	
]


 	