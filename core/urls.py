from django.urls import include, path
from core.views import (
    index,
    add_to_cart, 
    cart_view, 
    update_cart,
    delete_item_from_cart,
    filter_product, 
    product_list_view, 
    product_detail_view, 
    category_list_view, 
    category_product_list__view, 
    tag_list, 
    search_view,
    ajax_add_review,
    checkout_view,
    payment_completed_view,
    payment_failed_view,
    razorpay_payment_success_view,
    customer_dashboard,
    order_details
)

app_name = "core"

urlpatterns = [
    path("",index,name="index"),
    path("category/",category_list_view, name="category-list"),
    path("category/<cid>/",category_product_list__view, name="category-product-list"),
    path("products/",product_list_view, name="product-list"),
    path("products/tag/<slug:tag_slug>/",tag_list, name="tags"),
    path("product/<pid>/",product_detail_view, name="product-detail"),
    path("ajax-add-review/<int:pid>/",ajax_add_review, name="ajax-add-review"),
    path("search/",search_view,name="search"),
    path("filter-products/",filter_product,name="filter-products"),
    path("add-to-cart/",add_to_cart,name="add-to-cart"),
    path("update-cart/",update_cart,name="update-cart"),
    path("delete-from-cart/",delete_item_from_cart,name="delete-from-cart"),
    path("cart/",cart_view,name="cart"),
    path("checkout/",checkout_view,name="checkout"),
    path("paypal/",include("paypal.standard.ipn.urls")),
    path("payment-completed/",payment_completed_view, name="payment-completed"),
    path("payment-failed/",payment_failed_view, name="payment-failed"),
    path("razorpay-payment-success/",razorpay_payment_success_view, name="razorpay-payment-success"),
    path("dashboard/",customer_dashboard, name="dashboard"),
    path("dashboard/order/<int:id>",order_details, name="order-detail"),
]