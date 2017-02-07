
$(document).ready(function(){

	$('#taps').click(function(){
	    var productid;
	    productid = $(this).attr("data-productid");
	    $.get('/products/tap_product/', {product_id: productid}, function(data){
	               $('#tap_count').html(data);
	               $('#taps').hide();
	    });
	});

});

$(document).ready(function(){

	$('#trashes').click(function(){
	    var productid;
	    productid = $(this).attr("data-productid");
	    $.get('/products/trash_product/', {product_id: productid}, function(data){
	               $('#trash_count').html(data);
	               $('#trashes').hide();
	    });
	});

});