from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from core.models import Category,Products

def index(request):
    products= Products.objects.filter(product_status="published",featured=True)
    context = {"products":products}
    return render(request,'core/index.html',context)

def product_list_view(request):
    products= Products.objects.filter(product_status="published")
    context = {"products":products}
    return render(request,'core/product-list.html',context)

def category_list_view(request):
    categories= Category.objects.all()
    context = {"categories":categories}
    return render(request,'core/category-list.html',context)

def category_product_list__view(request,cid):
    category = Category.objects.get(cid=cid)
    products = Products.objects.filter(product_status="published",category=category)
    context = {"category":category,"products":products}
    return render(request,'core/category-product-list.html',context)

def product_detail_view(request,pid):
    product = Products.objects.get(pid=pid)
    related_products = Products.objects.filter(category=product.category).exclude(pid=pid)
    p_image = product.p_images.all()
    context = {"p":product,"p_image":p_image,"products":related_products}
    return render(request,'core/product-detail.html',context)