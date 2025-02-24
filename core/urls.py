from django.urls import path
from core.views import add_to_cart, cart_view, filter_product, product_list_view, product_detail_view, category_list_view, category_product_list__view, tag_list, index, ajax_add_review, search_view

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
    path("cart/",cart_view,name="cart"),
]