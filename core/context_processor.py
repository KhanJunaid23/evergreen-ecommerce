from django.db.models import Min, Max
from core.models import Address,Category,Products

def default(request):
    categories = Category.objects.all()
    min_max_price = Products.objects.aggregate(Min("price"),Max("price"))
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    return {
        'categories':categories,
        'address':address,
        'min_max_price':min_max_price
    }