
$(document).ready(function(){
	
	
$('a.taps').click(function(){
	var productid;
	productid = $(this).attr("data-productid");
	$.ajax({
	  url: '/products/tap_product/',
	  type: 'get',
	  
	  data: {'product_id': productid},
	  
	  success: function (data) {
	  	

	    $("#js-order-form").html(data.html_form);
	    $('.js-product-name').html(data.name);
	    $('#js-product-price').html(data.price);
	    $('#js-product-quantity').html(data.quantity);
		$('#js-product-description').html(data.description);
		$('#js-product-owner').html(data.owner);
		$('#js-owner-contact').html(data.contact);
		$('#js-owner-email').html(data.email);
		$('#js-owner-location').html(data.location);


	  }

 		});
 	});
});



	
	




$(document).ready(function(){

	$('a.trashes').click(function(){
	    var productid;
	    productid = $(this).attr("data-productid");
	    $.get('/products/trash_product/', {'product_id': productid}, function(data){
	               $('#trash_count').html(data);
	               
	    });
	});

});



$('body').on('submit', '#demo-bvd-notempty', function(){
	var form = $(this);
	
	
	$.ajax({

		url: form.attr('action'),
		type: form.attr('method'),
		data: form.serialize(),
		
		success: function(data){
			
			if (data.form_is_valid){
				console.log('Good work my boy!');
				$('#modal-tap').modal('hide');
				$('#modal-success').modal('show');
				
			}

			else{

				$('#js-order-form').html(data.html_form);
				
		
			}
			
		}
	});

	
	return false;
});





