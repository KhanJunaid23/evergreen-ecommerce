from core.models import Address,Category,Products,Wishlist
from django.contrib import messages
from django.db.models import Min, Max

def default(request):
    categories = Category.objects.all()
    min_max_price = Products.objects.aggregate(Min("price"),Max("price"))
    try:
        wishlist = Wishlist.objects.filter(user=request.user).count()
    except:
        messages.warning(request,"You need to login before accessing your wishlist.")
        wishlist = 0
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    return {
        'categories':categories,
        'address':address,
        'wishlist':wishlist,
        'min_max_price':min_max_price
    }