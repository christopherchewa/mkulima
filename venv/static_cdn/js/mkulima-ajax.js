
$(document).ready(function(){
	
	
	$('a.taps').click(function(){
	    var productid;
	    productid = $(this).attr("data-productid");
	    $.get('/products/tap_product/', {product_id: productid}, function(data){
	               $('#tap_count').html(data);
	               
	    });
	});

});



$(document).ready(function(){

	$('a.trashes').click(function(){
	    var productid;
	    productid = $(this).attr("data-productid");
	    $.get('/products/trash_product/', {product_id: productid}, function(data){
	               $('#trash_count').html(data);
	               
	    });
	});

});


$(document).ready(function(){

	$('.product-details').click(function(){
	    var productslug = $(this).attr("data-productslug");
	    

	    $.ajax({
	    	url: '/products/details/', 
	    	data: {'product_slug': productslug},
	    	dataType: 'json',
	    	type:'get',
	    	beforeSend: function() {
	    		$('#policy').modal('show');
	    	},
	    	

	    	success: function(data){
	               $('.js-product-name').html(data.name);
	               $('#js-product-price').html(data.price);
	               $('#js-product-description').html(data.description);
	               

	           }
	       
	       

	    
	    });
	});

});








$("#policy").on("submit", ".product-details", function () {
    var form = $(this);
    $.ajax({
      url: '/products/details/',
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        $('#policy').modal('hide');
      }
    });
     return false;
  });


