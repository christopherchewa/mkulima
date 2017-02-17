from django.contrib import admin
from .models import (
	AdminUserProfile,
	MkulimaUserProfile,
	
	Product,
	Order,



	)
# Register your models here.

admin.site.register(AdminUserProfile)
admin.site.register(MkulimaUserProfile)

admin.site.register(Product)
admin.site.register(Order)


