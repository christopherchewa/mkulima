from django.conf.urls import url
from . import views

# Create your models here.

urlpatterns = [

	#profile
	url(r'^adminprofile/(?P<pk>\d+)/edit/$', views.edit_profile_admin, name='edit-profile-admin'),
	url(r'^mkulimaprofile/(?P<pk>\d+)/edit/$', views.edit_profile_mkulima, name='edit-profile-mkulima'),
	url(r'^customerprofile/(?P<pk>\d+)/edit/$', views.edit_profile_customer, name='edit-profile-customer'),


	url(r'^products/$', views.product_list_view, name='product-list'),
	
	#ajax / customer
	url(r'^products/tap_product/$', views.tap_product, name='tap_product'),
	url(r'^products/trash_product/$', views.trash_product, name='trash_product'),

	url(r'^products/myorders/$', views.my_orders_view, name='my-orders'),



	#mkulima
	url(r'^orders/$', views.orders_view, name='orders'),
	url(r'^orders/(?P<pk>\d+)/clear/$', views.clear_order, name='clear_order'),

	

	#admin
	url(r'^adminpanel/(?P<pk>\d+)/remove/$', views.remove_sacco_members_view, name='remove-member'),
	url(r'^adminpanel/$', views.admin_panel, name='admin-panel'),
	url(r'^adminpanel/addmember/$', views.add_sacco_members_view, name='add-member'),
	url(r'^adminpanel/removelist/$', views.sacco_members_removelist, name='remove-list'),
	
	
	
	


	#Mkulima Panel
	url(r'^products/create/$', views.add_product_view, name = 'product-create'),
	url(r'^products/editlist/$', views.product_editlist, name='product-editlist'),
	url(r'^products/deletelist/$', views.product_deletelist, name='product-deletelist'),


	#mkulima
 	url(r'^products/(?P<slug>[\w-]+)/edit/$', views.edit_product_view, name = 'product-edit'),
 	url(r'^products/(?P<slug>[\w-]+)/delete/$', views.delete_product_view, name = 'product-delete'),
 	url(r'^mkulimapanel/$', views.mkulima_panel, name = 'mkulima-panel'),
	
 	
]


 	