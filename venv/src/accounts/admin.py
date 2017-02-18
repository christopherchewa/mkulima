from django.contrib import admin
from .models import (
	AdminUserProfile,
	MkulimaUserProfile,
	CustomerUserProfile,
	Product,
	Order,



	)
# Register your models here.

admin.site.register(AdminUserProfile)
admin.site.register(MkulimaUserProfile)
admin.site.register(CustomerUserProfile)
admin.site.register(Product)
admin.site.register(Order)


