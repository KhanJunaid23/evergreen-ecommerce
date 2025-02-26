const monthNames = ["Jan","Feb","Mar","April","May","June","July","Aug","Sept","Oct","Nov","Dec"];

$('#commentForm').submit(function(e){
    e.preventDefault();
    let dt = new Date();
    let time = dt.getDate() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear();
    $.ajax({
        data:$(this).serialize(),
        method:$(this).attr("method"),
        url:$(this).attr("action"),
        dataType:"json",
        success:function(response){
            if(response.bool== true){
                $('#review-res').html("Review added successfully.");
                $('.hide-comment-form').hide();
                $('.add-review').hide();

                let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                    _html +='<div class="user justify-content-between d-flex">'
                    _html +='<div class="thumb text-center">'
                    _html +='<img src="https://img.freepik.com/premium-vector/default-avatar-profile-icon-social-media-user-image-gray-avatar-icon-blank-profile-silhouette-vector-illustration_561158-3383.jpg" alt="" />'
                    _html +='<a href="#" class="font-heading text-brand">'+ response.context.user +'</a>'
                    _html +='</div>'

                    _html +='<div class="desc">'
                    _html +='<div class="d-flex justify-content-between mb-10">'
                    _html +='<div class="d-flex align-items-center">'
                    _html +='<span class="font-xs text-muted">'+ time +'</span>'
                    _html +='</div>'

                    for(let i =1; i <= response.context.rating; i++){
                        _html += '<i class="fas fa-star text-warning"></i>'
                    }

                    _html +='</div>'
                    _html +='<p class="mb-10">'+ response.context.review +'</p>'

                    _html +='</div>'
                    _html +='</div>'
                    _html +='</div>'
                $('.comment-list').prepend(_html)
            }
        }
    })
})


$(document).ready(function(){
    $(".filter-checkbox, #price-filter-btn").on("click", function(){
        let filter_object = {};
        let min_price = $("#max_price").attr("min");
        let max_price = $("#max_price").val();
        filter_object.min_price = min_price;
        filter_object.max_price = max_price;
        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val();
            let filter_key = $(this).data("filter");
            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key +']:checked')).map(function(element){
                return element.value
            })    
        })
        $.ajax({
            url:'/filter-products',
            data:filter_object,
            dataType:'json',
            beforeSend: function(){
                console.log("Sending Data.....");                
            },
            success: function(response){
                $("#filtered-product").html(response.data)
            }
        })
    })

    $('#max_price').on("blur", function(){
        let min_price = $(this).attr("min");
        let max_price = $(this).attr("max");
        let current_price = $(this).val();
        if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){
            min_price = Math.round(min_price*100)/100;
            max_price = Math.round(max_price*100)/100;
            alert("Price must be between ₹"+min_price+" and ₹"+max_price);
            $(this).val(min_price);
            $('#range').val(min_price);
            $(this).focus();
            return false;
        }
    })

    $(".add-to-cart-btn").on("click", function(){
        let this_val = $(this);
        let index = this_val.attr("data-index");
        let quantity = $(".product-quantity-"+index).val();
        let product_title = $(".product-title-"+index).val();
        let product_id = $(".product-id-"+index).val();
        let product_price = $(".current-product-price-"+index).text();
        let product_pid = $(".product-pid-"+index).val();
        let product_image = $(".product-image-"+index).val();
        $.ajax({
            url: '/add-to-cart',
            data:{
                'id':product_id,
                'pid':product_pid,
                'qty':quantity,
                'title':product_title,
                'price':product_price,
                'image':product_image,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("adding to cart....")
            },
            success: function(response){
                this_val.html("✓")
                $('.cart-items-count').text(response.totalcartitems)
            }
        })
    })
    
    $(document).on("click", '.delete-product', function(){
        let product_id = $(this).attr("data-product");
        let this_val = $(this);
        $.ajax({
            url: '/delete-from-cart',
            data:{
                'id':product_id
            },
            dataType: 'json',
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show();
                $('.cart-items-count').text(response.totalcartitems);
                $('#cart-list').html(response.data)
            }
        })
    })

    $(document).on("click", '.update-product', function(){
        let product_id = $(this).attr("data-product");
        let this_val = $(this);
        let product_quantity = $('.product-qty-'+product_id).val()
        console.log("product_id", product_id)
        console.log("product_quantity", product_quantity)
        $.ajax({
            url: '/update-cart',
            data:{
                'id':product_id,
                'qty':product_quantity
            },
            dataType: 'json',
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show();
                $('.cart-items-count').text(response.totalcartitems);
                $('#cart-list').html(response.data)
            }
        })
    })

    $(document).on("click", '.make-default-address', function(){
        let id = $(this).attr("data-address-id");
        let this_val = $(this);
        $.ajax({
            url:'/make-default-address',
            data:{
                "id":id
            },
            dataType:'json',
            success: function(response){
                if(response.boolean == true){
                    $(".check").hide();
                    $(".action_btn").show();
                    $(".check"+id).show();
                    $(".button"+id).hide();
                }
            }
        })
    })

    $(document).on("click", '.add-to-wishlist', function(){
        let product_id = $(this).attr("data-product-item");
        let this_val = $(this);
        $.ajax({
            url:"/add-to-wishlist",
            data:{
                "id":product_id
            },
            dataType:"json",
            beforeSend: function(){
                console.log("Adding to Wishlist")
            },
            success: function(response){
                this_val.html("✓");
                if(response.bool == true){
                    console.log("Added to Wishlt")
                }
            }
        })
    })
})