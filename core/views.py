import razorpay
import time
from core.forms import ProductReviewForm
from core.models import Category,Products,ProductReview,CartOrder,CartOrderItems, Address
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from taggit.models import Tag

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

def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid']
    }
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data":request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj'])})

def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request,'core/cart.html',{"cart_data":request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj']),"cart_total_amount":cart_total_amount})
    else:
        messages.warning(request,"Your Cart is empty")
        return redirect("core:index")

def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    context = render_to_string("core/async/cart-list.html",{"cart_data":request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj']),"cart_total_amount":cart_total_amount})
    return JsonResponse({"data":context, "totalcartitems": len(request.session['cart_data_obj'])})   

def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[product_id]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    context = render_to_string("core/async/cart-list.html",{"cart_data":request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj']),"cart_total_amount":cart_total_amount})
    return JsonResponse({"data":context, "totalcartitems": len(request.session['cart_data_obj'])})          

@login_required
def checkout_view(request):
    cart_total_amount = 0
    total_amount = 0
    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])
        order = CartOrder.objects.create(user=request.user,price=total_amount)
        for pid, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            cart_product_items = CartOrderItems.objects.create(
                order=order,
                invoice_no="INVOICE_NO_"+str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty'])*float(item['price'])
            )
    razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order = razorpay_client.order.create({
        "amount": cart_total_amount*100,
        "currency": "INR",
        "payment_capture": "1",
    })
    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except:
        messages.warning(request,"There are multiple addresses, only one should be activated.")
        active_address = None
    return render(request, 'core/checkout.html', {"cart_data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj']), "cart_total_amount": cart_total_amount,"razorpay_order_id": razorpay_order['id'],"razorpay_key": settings.RAZORPAY_KEY_ID,"currency": "INR","active_address":active_address})

@csrf_exempt
@login_required
def payment_completed_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    return render(request, 'core/payment-completed.html', {"cart_data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj']), "cart_total_amount": cart_total_amount})

def payment_failed_view(request):
    return render(request,"core/payment-failed.html")

@csrf_exempt
def razorpay_payment_success_view(request):
    return render(request, 'core/razorpay-payment-success.html')

@login_required
@csrf_exempt
def customer_dashboard(request):
    orders = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)
    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("phone")
        new_address = Address.objects.create(user=request.user,address=address,mobile=mobile)
        messages.success(request,"Address added successfully")
        return redirect("core:dashboard")
    context = {"orders":orders,"address":address}
    return render(request,"core/dashboard.html",context)

def order_details(request,id):
    order = CartOrder.objects.get(user=request.user,id=id)
    order_items = CartOrderItems.objects.filter(order=order)
    context = {"order_items":order_items}
    return render(request, 'core/order-detail.html', context)

def make_address_default(request):
    id = request.GET['id']
    Address.objects.filter(user=request.user).update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean":True})