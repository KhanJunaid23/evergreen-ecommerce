from django.urls import path
from core.views import product_list_view, category_list_view, category_product_list__view, index

app_name = "core"

urlpatterns = [
    path('',index,name='index'),
    path('category/',category_list_view, name='category-list'),
    path('category/<cid>/',category_product_list__view, name='category-product-list'),
    path('products/',product_list_view, name='product-list'),
]