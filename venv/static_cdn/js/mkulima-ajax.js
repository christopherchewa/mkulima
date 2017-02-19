



$('#js-order-form').on('submit', '#demo-bvd-notempty', function(){
	var form = $(this)
	var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
	var productslug;
	productslug = $('a.taps').attr("data-productslug");
	$.ajax({

		url: '/products/tap_product/',
		type: 'post',
		beforeSend : function(jqXHR, settings) {
        jqXHR.setRequestHeader("x-csrftoken", get_the_csrf_token_from_cookie());
    	
    	},

		data: { 

			product_slug : {'product_slug': productslug},
		 	form : form.serialize(),
		 	csrfmiddlewaretoken: {'csrfmiddlewaretoken': token},
		},

		dataType: 'json',
	
		
		

		success: function(data){
			
			if (data.form_is_valid){
				console.log('post-success');
				alert("Successfull order!");
			}
			else{

				$('#js-order-form').html(data.html_form);
			}
			
			
		}
	});

	
	return false;
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
		$('#js-product-description').html(data.description);

	  }

 		});
 	});
});


