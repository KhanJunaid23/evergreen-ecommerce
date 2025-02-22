from core.models import Address,Category

def default(request):
    categories = Category.objects.all()
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    return {
        'categories':categories,
        'address':address
    }