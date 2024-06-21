from storeapp.models import Cart, Product, Category, Vendor, Address, WishList
import uuid
# We import Min and Max method to get min and max figures
from django.db.models import Min, Max
from django.contrib import messages


# Function to be passed to all template in frontend view
def default(request):
    categories = Category.objects.all()

    vendors = Vendor.objects.all()

    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))

    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None

    try:
        wishlist = WishList.objects.filter(user=request.user)
    except TypeError:
        #messages.warning(request, "You need to login to access wishlists")
        wishlist = 0

    return {
        'categories': categories,
        'wishlist': wishlist,
        'address': address,
        'vendors': vendors,
        'min_max_price': min_max_price,
    }


def cart_render(request):
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user, completed=False)
            #cartitems = cart.cartitems.all()
        else:
            cart = Cart.objects.get(
                session_id=request.session['nonuser'], completed=False)
            #cartitems = cart.cartitems.all()

    except:
        cart = {"num_of_item": 0}
        #cartitems = cart.cartitems.all()

    return {"cart": cart}  # "cartitems": cartitems}
