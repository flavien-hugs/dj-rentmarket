$(document).ready(function(){
	// using jQuery
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	var csrftoken = getCookie('csrftoken');

	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});

	// Cart + Add Products 
	var productForm = $(".product__actions");
	function getOwnedProduct(productId, submitSpan){
		var actionEndpoint = '/orders/endpoint/verify/ownership/'
		var httpMethod = 'GET';
		var data = {product_id: productId}

		var isOwner;
		$.ajax({
			url: actionEndpoint,
			method: httpMethod,
			data: data,
			success: function(data){
				console.log(data)
				console.log(data.owner)
				if (data.owner){
					isOwner = true
					submitSpan.html("<a class='btn btn-warning' href='/library/'>In Library</a>")
				} else {
					isOwner = false
				}
			},
			error: function(erorr){
			  console.log(error)
			}
		});
		return isOwner
	}

	$.each(productForm, function(index, object){
		var $this = $(this)
		var isUser = $this.attr("data-user")
		var submitSpan = $this.find(".submit")
		var productInput = $this.find("[name='product_id']")
		var productId = productInput.attr("value")

		if (isUser){
			var isOwned = getOwnedProduct(productId, submitSpan)
		}
	})  

	productForm.submit(function(event){
		event.preventDefault();
		var thisForm = $(this)
		var actionEndpoint = thisForm.attr("data-endpoint")
		var httpMethod = thisForm.attr("method");
		var formData = thisForm.serialize();

		$.ajax({
			url: actionEndpoint,
			method: httpMethod,
			data: formData,
			success: function(data){
				var submitSpan = thisForm.find(".submit")
				if (data.added){
					submitSpan.html("<div class='product__actions-item product__actions-item--addtocart submit'> <a href='/location/detail/' class='btn btn-primary btn-lg'>Delete ?</a> </div>")
				} else {
					submitSpan.html("<button type='submit' class='btn btn-primary btn-lg'>louer</button>")
				}
				
				var navbarCount = $(".location_items_count")
				navbarCount.text(data.LocationItemCount)
				var currentPath = window.location.href

				if (currentPath.indexOf("location") != -1) {
					refreshCart()
				}
			},
			error: function(errorData){
				$.alert({
					title: "Oops!",
					content: "An error occurred",
					theme: "modern",
				})
			}
		})
	})

	function refreshCart(){
		console.log("in current cart")
		var cartTable = $(".cart-table")
		var cartBody = cartTable.find(".cart-body")
		var productRows = cartBody.find(".cart-table__row")
		var currentUrl = window.location.href

		var refreshCartUrl = '/api/location/'
		var refreshCartMethod = "GET";
		var data = {};
		$.ajax({
			url: refreshCartUrl,
			method: refreshCartMethod,
			data: data,

			success: function(data){
				var hiddenLocationItemRemoveForm = $(".remove_location")
				if (data.product.length > 0){
					productRows.html(" ")
					i = data.product.length
					
					$.each(data.product, function(index, value){
						console.log(value)
						var newLocationItemRemove = hiddenLocationItemRemoveForm.clone()
						newLocationItemRemove.css("display", "block")
						newLocationItemRemove.find(".remove_location").val(value.id)
						cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.name + "</a>" + newLocationItemRemove.html() + "</td><td>" + value.price + "</td></tr>")
						i --
					})
			
					cartBody.find(".cart-subtotal").text(data.subtotal)
					cartBody.find(".cart-total").text(data.total)
				} else {
					window.location.href = currentUrl
				}
		
			},
			error: function(errorData){
				$.alert({
					title: "Oops!",
					content: "An error occurred",
					theme: "modern",
				})
			}
		})
	}
});