from accounts.models import Order, Product, CustomerUserProfile



class ReferMiddleware():

	def process_request(self, request):

		product_id = request.GET.get("product_id")
		
		try:
			obj = Product.objects.get(id=product_id)
		except:
			obj = None
		if obj:
			request.session['product_id_ref'] = obj.id
			
			
			

			