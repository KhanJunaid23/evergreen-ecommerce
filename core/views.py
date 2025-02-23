from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from taggit.models import Tag
from core.models import Category,Products,ProductReview
from core.forms import ProductReviewForm

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
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    review_form = ProductReviewForm()
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user,product=product).count()
        if user_review_count > 0:
            make_review = False
    p_image = product.p_images.all()
    context = {"p":product,"review_form":review_form,"make_review":make_review,"p_image":p_image,"products":related_products,"reviews":reviews,"average_rating":average_rating}
    return render(request,'core/product-detail.html',context)

def tag_list(request,tag_slug=None):
    products = Products.objects.filter(product_status="published")
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        products = products.filter(tags__in=[tag])
    context = {"products":products,"tag":tag}
    return render(request,'core/tag.html',context)

def ajax_add_review(request,pid):
    product = Products.objects.get(pk=pid)
    user = request.user
    review = ProductReview.objects.create(user=user,product=product,review=request.POST['review'],rating=request.POST['rating'])
    context = {"user":user.username,"review":request.POST['review'],"rating":request.POST['rating']}
    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    return JsonResponse({'bool':True,'context':context,'average_reviews':average_reviews})

def search_view(request):
    query = request.GET.get("q")
    products = Products.objects.filter(title__icontains=query).order_by("-added_date")
    context={"products":products,"query":query}
    return render(request,'core/search.html',context)

def filter_product(request):
    categories = request.GET.getlist("category[]")
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']
    products = Products.objects.filter(product_status="published").order_by("-id").distinct()
    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)
    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()
    data = render_to_string("core/async/product-list.html",{"products":products})
    return JsonResponse({"data":data})

