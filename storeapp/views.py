import json
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from ast import Add
from django.urls import reverse

from conversation.models import Conversation
from . models import Address, Cart, CartItem, Product, Category, Vendor, ProductReview, WishList, CartOrder
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
# Complex Query to query multiple fields
from django.db.models import Q, Count, Avg
from django.core import serializers
from . import context_processors
from .forms import UpdateUserForm, ProductReviewForm
from userapp.forms import VendorNewItemForm, EditProductForm
from userapp.models import ContactUs, User, Profile
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from storeapp.context_processors import default
from django.template.loader import render_to_string
from django.core import serializers

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

import calendar
from django.db.models.functions import ExtractMonth

# REMOVE THIS BELOW WHEN U CLARIFY THE AB0VE IMPORT
#PayPalPaymentsForm = 0


# Create your views here.


def index(request):

    # cart, created = Cart.objects.get_or_create(user=request.user, completed=False)  # GET OR CREATE CART FOR LOGGED IN USER
    # GET ALL THE CART ATTRIBUTES FROM THE (CART-ITEM OBJECT LINKED TO CART CLASS THROUGH RELATED-NAME) AND NOT FROM CART'S OBJECT

    context = {
        # "cartitems": cartitems,
        # "cart": cart
    }
    return render(request, "index.html", context)

# FOR THE PRODUCT DETAIL


def detail(request, slug):
    vendors = Vendor.objects.all()
    categories = Category.objects.all()
    products = Product.objects.all()
    try:
        product = Product.objects.get(slug=slug, gadgets="False")
    except:
        messages.warning(request, "Pls search at the appropriate shopping section")
        return redirect("storeapp:products")    

    # getting average rating
    average_rating = ProductReview.objects.filter(
        product=product).aggregate(rating=Avg('rating'))

    # getting related products
    rp = Product.objects.filter(category=product.category).exclude(slug=slug)

    # getting reviews ordering from latest to oldest
    reviews = ProductReview.objects.filter(product=product).order_by("-date")


    user_profile = None
    if request.user.is_authenticated:
    # Getting loggedin user image
        user_profile = Profile.objects.get(user=request.user)

   
    # getting the review form from forms.py
    review_form = ProductReviewForm()

    # to enable logged in user make review once per product-item
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(
            user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False
  

    #GETTING RECENTLY VIEWED PRODUCTS
    recently_viewed_products = None
    # similar_products = Product.objects.filter(category = products.category).exclude(slug=product.slug)
    # cart, created = Cart.objects.get_or_create(user=request.user, completed=False)  # GET OR CREATE CART FOR LOGGED IN USER

    if 'recently_viewed' in request.session:
        # IF A PRODUCT IS IN RECENTLY VIEWED
        if slug in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(slug)  # REMOVE IT

        products = Product.objects.filter(
            slug__in=request.session['recently_viewed'])
        recently_viewed_products = sorted(
            products, key=lambda x: request.session['recently_viewed'].index(x.slug))

        # TO TAAKE A VIEWED PRODUCT TO THE BEGINNING OF THE LIST
        request.session['recently_viewed'].insert(0, slug)
        if len(request.session['recently_viewed']) > 4:
            # REMOVE LAST ITEM, LET TOTAL LIST BE 4
            request.session['recently_viewed'].pop()
    else:
        request.session['recently_viewed'] = [slug]

    request.session.modified = True  # DJANGO SHOULD AUTO UPDATE

    context = {
        "product": product,
        "products": products,
        "recently_viewed_products": recently_viewed_products,
        # "cart": cart,
        "reviews": reviews,
        "user_profile":user_profile,
        "make_review": make_review,
        "review_form": review_form,
        "rp": rp,
        "average_rating": average_rating,
        "vendors": vendors,
        "categories": categories
        # "similar_products":similar_products,
    }
    return render(request, "detail.html", context)


# View to Handle Tags
def tag_list(request, tag_slug=None):
    products = Product.objects.all().order_by('id')

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)

        # get product that share same tags
        products = products.filter(tags__in=[tag])
    context = {
        'products': products,
        'tag': tag,
    }
    return render(request, "tags.html", context)


# View to Handle Tags
def tag_show(request, tag_slug=None):
    products = Product.objects.all().order_by('id')

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)

        # get product that share same tags
        products = products.filter(tags__in=[tag])
    context = {
        'products': products,
        'tag': tag,
    }
    return render(request, "filter-sec.html", context)

# Function to write a review on a product
def ajax_add_review(request, id):
    product = Product.objects.get(id=id)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=request.POST['rating']
    )

    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating']
    }

    # Getting the average review
    average_reviews = ProductReview.objects.filter(
        product=product).aggregate(rating=Avg('rating'))

    return JsonResponse(
        {
            'bool': True,
            'context': context,
            'average_reviews': average_reviews
        }
    )


def review_likes(request, id):
    if request.user.is_authenticated:
        review = get_object_or_404(ProductReview, id=id)
        #if like has been done by authenticatd user, remove like
        if review.likes.filter(id=request.user.id):
            review.likes.remove(request.user)
        else:
            review.likes.add(request.user)    

        return redirect("storeapp:detail", review.product.slug)
    else:
        review = get_object_or_404(ProductReview, id=id)
        messages.warning(request, "You must be logged in to like review!!!")
        return redirect("storeapp:detail", review.product.slug)
    
    context = {
        "review":review
    } 

    return render(request, "detail.html", context)       



def category_list(request):
    # cart, created = Cart.objects.get_or_create(user=request.user, completed=False)  # GET OR CREATE CART FOR LOGGED IN USER
    # GET ALL THE CART ATTRIBUTES FROM THE (CART-ITEM OBJECT LINKED TO CART CLASS THROUGH RELATED-NAME) AND NOT FROM CART'S OBJECT
    #cartitems = cart.cartitems.all()
    categories = Category.objects.all()
    context = {
        "categories": categories,
        # 'cart': cart,
        # 'cartitems': cartitems,
    }

    return render(request, "categories.html", context)


def category_detail(request, id):
    # cart, created = Cart.objects.get_or_create(user=request.user, completed=False)  # GET OR CREATE CART FOR LOGGED IN USER
    # GET ALL THE CART ATTRIBUTES FROM THE (CART-ITEM OBJECT LINKED TO CART CLASS THROUGH RELATED-NAME) AND NOT FROM CART'S OBJECT
    #cartitems = cart.cartitems.all()
    category = Category.objects.get(id=id)
    cat_products = Product.objects.filter(category=category, in_stock="True")
    #products = Category.objects.filter(slug=category)
    vendors = Vendor.objects.all()
    #rp = Category.objects.filter(products=cat_products).exclude(id=id)



    context = {
        'category': category,
        #'rp':rp,
        # 'cart': cart,
        # 'cartitems': cartitems,
        #'products': products,
        'cat_products':cat_products,
        'vendors': vendors
    }

    return render(request, "category_detail.html", context)


# CART FOR USER


def cart(request):
    # cart = None  # TO PREVENT ERRORS BASED ON THE FACT THAT UNAUTHENTICATED USERS CANNOT ADD TO CART OR CREATED CART
    cartitems = []  # TO PREVENT ERRORS JUST AS ABOVE
    # GET ALL THE CART ATTRIBUTES FROM THE (CART-ITEM OBJECT LINKED TO CART CLASS THROUGH RELATED-NAME) AND NOT FROM CART'S OBJECT
    #cartitems = cart.cartitems.all()

    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user, completed=False)
            cartitems = cart.cartitems.all()

        else:
            cart = Cart.objects.get(
                session_id=request.session['nonuser'], completed=False)
            if cartitems:
                cartitems = cart.cartitems.all()
            else:
                cart = Cart.objects.get(
                    session_id=request.session['nonuser'], completed=False)
                cartitems = cart.cartitems.all()

    except:
        try:
            cart = Cart.objects.get(
                session_id=request.session['nonuser'], completed=False)
            cartitems = cart.cartitems.all()
        except:
            cart = {"num_of_item": 0}

    context = {

        "cartitems": cartitems,
        "cart": cart
    }
    return render(request, "cart.html", context)


# TO ADD TO CART FUNCTION
def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    #game_id = data["id"]
    #gadget_id = data["id"]
    product = Product.objects.get(id=product_id)
    #game = Product.objects.get(id=game_id)
    #gadget = Product.objects.get(id=gadget_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user, completed=False)
        cartitem, created = CartItem.objects.get_or_create(
            cart=cart, product=product)
        cartitem.quantity += 1
        cartitem.save()
        num_of_item = cart.num_of_item  # FROM MODELS

    else:
        try:
            cart = Cart.objects.get(
                session_id=request.session['nonuser'], completed=False)
            cartitem, created = CartItem.objects.get_or_create(
                cart=cart, product=product)
            cartitem.quantity += 1
            cartitem.save()
            num_of_item = cart.num_of_item

        except:
            request.session['nonuser'] = str(uuid.uuid4())
            cart = Cart.objects.create(
                session_id=request.session['nonuser'], completed=False)
            cartitem, created = CartItem.objects.get_or_create(
                cart=cart, product=product)
            cartitem.quantity += 1
            cartitem.save()
            num_of_item = cart.num_of_item

        num_of_item = cart.num_of_item

        print(cartitem)
    return JsonResponse(num_of_item, safe=False)

    # ADD TO CART WITH SESSION
# def add_to_cart(request):
    # data = json.loads(request.body)  # FROM THE AJAX BODY
    # ACCESSING PRODUCT_ID IN AJAX WITH ID(STRING) AND PASSING TO THE VARIABLE
    # product_id = data['id']
    # GET PRODUCT WITH THAT ID FROM DB
    # product = Product.objects.get(id=product_id)
    # GET PRODUCT WITH THAT ID FROM DB
    # nonuser_cart = Cart.objects.get(
    # session_id=request.session['nonuser'], completed=False)
    # action = data['action']
    # cart= Cart.objects.get(session_id = request.session['nonuser'], completed=False)
    # cartitems = cart.cartitems_set.all()
    # IF USER IS LOGGEDIN GET OR CREATE CARTITEM WITH CART AND PRODUCT FROM DB
    # if action == 'add':
    # message = {
    #    'num_of_item' : cart.num_of_item
    # }


# PRODUCTS VIEW
def products(request):
    # if request.user.is_authenticated:  # IF USER IS LOGGED IN
    # cart, created = Cart.objects.get_or_create(user=request.user, completed=False)  # GET OR CREATE CART FOR LOGGED IN USER
    if 'search' in request.GET:
        search = request.GET['search']
        # products = Product.objects.filter(name__icontains=search)
        multiple_queries = Q(Q(name__icontains=search) |
                             Q(slug__icontains=search))
        products = Product.objects.filter(multiple_queries)
    else:
        products = Product.objects.filter(
            vendor_product="False", women="False", gadgets="False", games="False")
    context = {
        "products": products,
        #    "nonuser_cart":nonuser_cart
    }
    return render(request, "products.html", context)


def filter_product(request):
    # To get categorues and vendors ticks from user input
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.all().order_by("-id").distinct()

    # filter tru available product get price >= min price tru "price" lookup field
    products = products.filter(price__gte=min_price)
    # filter tru available product get price <= max price tru "price" lookup field
    products = products.filter(price__lte=max_price)

    if len(categories) > 0:
        # Checks if category has id object "in" ( is a django inbuilt func) our declared var "categories"
        products = products.filter(category__id__in=categories).distinct()

    if len(vendors) > 0:
        # Checks if category has id object "in" ( is a django inbuilt func) our declared var "categories/vendors"
        vendors = products.filter(vendor__id__in=vendors).distinct()


    context = {
        "products": products,
    }

    data = render_to_string("async/product-list.html", context)
    return JsonResponse({"data": data})


def women(request):
    # if request.user.is_authenticated:  # IF USER IS LOGGED IN
    # cart, created = Cart.objects.get_or_create(user=request.user, completed=False)  # GET OR CREATE CART FOR LOGGED IN USER
    #products = Product.objects.filter(women="True", vendor_product="False")
    if 'search' in request.GET:
        search = request.GET['search']
        # products = Product.objects.filter(name__icontains=search)
        multiple_queries = Q(Q(name__icontains=search) |
                             Q(slug__icontains=search))
        products = Product.objects.filter(multiple_queries)
    else:
        products = Product.objects.filter(women="True", vendor_product="False")

    context = {
        # "cart": cart,
        "products": products
    }

    return render(request, "women.html", context)


def women_detail(request, slug):
    vendors = Vendor.objects.all()
    categories = Category.objects.all()
    try:
        product = Product.objects.get(id=slug, women="True")
    except:
        messages.warning(request, "Pls search at the appropriate shopping section")
        return redirect("storeapp:women")    
    recently_viewed_products = None

    # cart, created = Cart.objects.get_or_create(
    # user=request.user, completed=False)  # GET OR CREATE CART FOR LOGGED IN USER

    # getting related products
    rp = Product.objects.filter(category=product.category).exclude(slug=slug)

    # getting reviews ordering from latest to oldest
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    # getting the review form from forms.py
    review_form = ProductReviewForm()

    # to enable logged in user make review once per product-item
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(
            user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False


    #  GETTING RECENTLY VIEWED PRODUCTS
    recently_viewed_products = None
    if 'recently_viewed' in request.session:
        # IF A PRODUCT IS IN RECENTLY VIEWED
        if slug in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(slug)  # REMOVE IT

        products = Product.objects.filter(slug__in=request.session['recently_viewed'])
        recently_viewed_products = sorted(
            products, key=lambda x: request.session['recently_viewed'].index(x.slug))

        # TO TAAKE A VIEWED PRODUCT TO THE BEGINNING OF THE LIST
        request.session['recently_viewed'].insert(0, slug)
        if len(request.session['recently_viewed']) > 4:
            # REMOVE LAST ITEM, LET TOTAL LIST BE 4
            request.session['recently_viewed'].pop()
    else:
        request.session['recently_viewed'] = [slug]

    request.session.modified = True  # DJANGO SHOULD AUTO UPDATE

    context = {
        "product": product,
        # "cart": cart,
        "recently_viewed_products": recently_viewed_products,
        "vendors": vendors,
        "categories": categories,
        "rp": rp,
        "reviews": reviews,
        "review_form": review_form
    }

    return render(request, "women_detail.html", context)


# GAMES VIEW
def games(request):
    products = Product.objects.filter(games="True", vendor_product="False")   
    # nonuser_cart = None
    # if 'nonuser' in request.session:
    #    nonuser_cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
    # if request.user.is_authenticated:  # IF USER IS LOGGED IN
    # cart, created = Cart.objects.get_or_create(
    # user=request.user, completed=False)  # GET OR CREATE CART FOR LOGGED IN USER
    if 'search' in request.GET:
        search = request.GET['search']
        # products = Product.objects.filter(name__icontains=search)
        multiple_queries = Q(Q(name__icontains=search) |
                             Q(slug__icontains=search))
        products = Product.objects.filter(multiple_queries)
    else:
        products = Product.objects.filter(games="True", vendor_product="False")
    context = { 
        "products": products,
        # "cart": cart,
        # "nonuser_cart":nonuser_cart
    }
    return render(request, "games.html", context)
# FOR THE GAMES DETAIL


def gamesdetail(request, slug):
    try:
        game = Product.objects.get(slug=slug, games="True")
    except:
        messages.warning(request, "Pls search at the appropriate shopping section")
        return redirect("storeapp:games")     
    vendors = Vendor.objects.all()
    categories = Category.objects.all()
    recently_viewed_games = None

    # cart, created = Cart.objects.get_or_create(
    # user=request.user, completed=False)  # GET OR CREATE CART FOR LOGGED IN USER

    if 'recently_viewed' in request.session:
        # IF A PRODUCT IS IN RECENTLY VIEWED
        if slug in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(slug)  # REMOVE IT

        games = Product.objects.filter(slug__in=request.session['recently_viewed'])
        recently_viewed_games = sorted(games,
                                       key=lambda x: request.session['recently_viewed'].index(
                                           x.slug)
                                       )

        # TO TAKE A VIEWED PRODUCT TO THE BEGINNING OF THE LIST
        request.session['recently_viewed'].insert(0, slug)
        if len(request.session['recently_viewed']) > 4:
            # REMOVE LAST ITEM, LET TOTAL LIST BE 4
            request.session['recently_viewed'].pop()
    else:
        request.session['recently_viewed'] = [slug]

    request.session.modified = True  # DJANGO SHOULD AUTO UPDATE
    
    
    # getting average rating
    average_rating = ProductReview.objects.filter(
        product=game).aggregate(rating=Avg('rating'))

    # getting related products
    rp = Product.objects.filter(category=game.category).exclude(slug=slug)

    # getting reviews ordering from latest to oldest
    reviews = ProductReview.objects.filter(product=game).order_by("-date")

    # getting the review form from forms.py
    review_form = ProductReviewForm()

    # to enable logged in user make review once per product-item
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(
            user=request.user, product=game).count()

        if user_review_count > 0:
            make_review = False
    
    
    context = {
        "game": game,
        "recently_viewed_games": recently_viewed_games,
        # "cart": cart,
        "vendors": vendors,
        "categories": categories,
        'average_rating': average_rating,
        'rp': rp,
        'reviews': reviews,
        'review_form': review_form
    }
    return render(request, "gamesdetail.html", context)


# GADGET VIEW
def gadgets(request):
    products = Product.objects.filter(gadgets="True", vendor_product="False")
    # if request.user.is_authenticated:  # IF USER IS LOGGED IN
    # cart, created = Cart.objects.get_or_create(user=request.user, completed=False)  # GET OR CREATE CART FOR LOGGED IN USER
    if 'search' in request.GET:
        search = request.GET['search']
        # products = Product.objects.filter(name__icontains=search)
        multiple_queries = Q(Q(name__icontains=search) |
                             Q(slug__icontains=search))
        products = Product.objects.filter(multiple_queries)
    else:
        products = Product.objects.filter(
            gadgets="True", vendor_product="False")
    context = {
        "products": products,
        # "cart": cart
    }
    return render(request, "gadgets.html", context)


# FOR THE GADGETS DETAIL
def gadgetsdetail(request, slug):
    try:
        gadget = Product.objects.get(slug=slug, gadgets="True")
    except:
        messages.warning(request, "Pls search at the appropriate shopping section")
        return redirect("storeapp:gadgets")    
    vendors = Vendor.objects.all()
    products = Product.objects.all()
    categories = Category.objects.all()

    recently_viewed_gadgets = None

    # cart, created = Cart.objects.get_or_create(user=request.user, completed=False)  # GET OR CREATE CART FOR LOGGED IN USER
    # if request.user.is_authenticated:  # IF USER IS LOGGED IN
    # cart, created = Cart.objects.get_or_create(
    # user=request.user, completed=False)  # GET OR CREATE CART FOR LOGGED IN USER

    if 'recently_viewed' in request.session:
        # IF A PRODUCT IS IN RECENTLY VIEWED
        if slug in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(slug)  # REMOVE IT

        gadgets = Product.objects.filter(
            slug__in=request.session['recently_viewed'])
        recently_viewed_gadgets = sorted(gadgets,
                                         key=lambda x: request.session['recently_viewed'].index(
                                             x.slug)
                                         )

        # TO TAAKE A VIEWED PRODUCT TO THE BEGINNING OF THE LIST
        request.session['recently_viewed'].insert(0, slug)
        if len(request.session['recently_viewed']) > 4:
            # REMOVE LAST ITEM, LET TOTAL LIST BE 4
            request.session['recently_viewed'].pop()
    else:
        request.session['recently_viewed'] = [slug]

    request.session.modified = True  # DJANGO SHOULD AUTO UPDATE

    # getting average rating
    average_rating = ProductReview.objects.filter(
        product=gadget).aggregate(rating=Avg('rating'))

    # getting related products
    rp = Product.objects.filter(category=gadget.category).exclude(slug=slug)

    # getting reviews ordering from latest to oldest
    reviews = ProductReview.objects.filter(product=gadget).order_by("-date")

    # getting the review form from forms.py
    review_form = ProductReviewForm()

    # to enable logged in user make review once per product-item
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(
            user=request.user, product=gadget).count()

        if user_review_count > 0:
            make_review = False

    context = {
        "gadget": gadget,
        "recently_viewed_gadgets": recently_viewed_gadgets,
        # "cart": cart,
        "products": products,
        "vendors": vendors,
        "categories": categories,
        "average_rating": average_rating,
        "rp": rp,
        "reviews": reviews,
        "review_form": review_form

    }
    return render(request, "gadgetsdetail.html", context)


# DASHBOARD SECTION
@login_required
def dashboard(request):
    #cart = Cart.objects.get(session_id=request.session['nonuser'], completed=False)
    #cartitems = cart.cartitems.all()
    #cartitems = 0
    order_list = None
    address = None

    if request.user.is_authenticated:
        order_list = Cart.objects.filter(user=request.user).order_by("-id")
        #cartitems = orders.cartitems.all()
        address = Address.objects.filter(user=request.user)
        orders = Cart.objects.annotate(month=ExtractMonth("created_on")).values(
            "month").annotate(count=Count("id")).values("month", "count")
        month = []
        total_orders = []
        for i in orders:
            month.append(calendar.month_name[i["month"]])
            total_orders.append(i["count"])

        if request.method == "POST":
            address = request.POST['address']
            mobile = request.POST['mobile']

            new_address = Address.objects.create(
                user=request.user,
                address=address,
                mobile=mobile,
            )
            messages.success(request, "Address added successfully...")
            return redirect('storeapp:dashboard')
        else:
            print("Error")       
        try:
            user_profile = Profile.objects.get(user=request.user)
        except:
            user_profile = Profile.objects.create(
                user=request.user
            )     
    else:
        messages.warning(request, 'Login to access dashboard')
        return redirect('storeapp:home')    


    context = {
        'user_profile': user_profile,
        'order_list': order_list,
        'address': address,
        'orders': orders,
        # 'cartitems': cartitems
    }
    return render(request, "dashboard.html", context)


# SETTINGS VIEW
def settings(request):
    return render(request, "settings.html")


def make_default_address(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})



def order_detail(request, id):
    if request.user.is_authenticated:
        order = Cart.objects.get(user=request.user, id=id)
        order_items = CartItem.objects.filter(cart=order)
    context = {
        'order_items': order_items
    }
    return render(request, "order_detail.html", context)


def wishlist(request):
    if request.user.is_authenticated:
        wishlist = WishList.objects.filter(user=request.user)
    else:
        messages.warning(request, "Login to access wishlist")
        return redirect("storeapp:home")
 
    context = {
        "wishlist": wishlist,
    }

    return render(request, "wishlist.html", context)


def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    print("Product ID is:" + product_id)

    context = {}

    wishlist_count = WishList.objects.filter(
        product=product, user=request.user).count()
    print(wishlist_count)

    if wishlist_count > 0:
        context = {
            "bool": True
        }
    else:
        new_wishlist = WishList.objects.create(
            user=request.user,
            product=product,
        )
        context = {
            "bool": True
        }

    return JsonResponse(context)


def remove_wishlist(request):
    pid = request.GET['id']
    wishlist = WishList.objects.filter(user=request.user)
    wishlist_id = WishList.objects.get(id=pid)
    delete_product = wishlist_id.delete()

    context = {
        "bool": True,
        "wishlist": wishlist
    }
    wishlist_json = serializers.serialize('json', wishlist)
    data = render_to_string("async/wishlist-list.html", context)
    return JsonResponse({'data': data, 'wishlist': wishlist_json})


# DELETE CART ITEM
def delete_cartitem_view(request, id):
    #cart = get_object_or_404(CartItem, pk=id)
    cartitem = CartItem.objects.get(id=id)

    cartitem.delete()
    return redirect("storeapp:cart")
    #return render(request, "cart.html")





#def delete_cart_item(request):
    #cart = Cart.objects.all()
    #num_of_items = cartitems = cart.cartitems.all()
    #totalcartitems = num_of_items

    #if 'id' in request.GET:
    #pid = request.GET['id']
    #product = Cart.objects.get(id=pid)
    #cart = Cart.objects.filter(user=request.user)
    #cart_item = CartItem.objects.get(cart=cart, product=product)
    #delete_cart_item = product.delete()  

    #context = {
    #    "bool": True,
    #    "cart": cart
    #}
    #cart_json = serializers.serialize('json', cart)
    #data = render_to_string("async/cart-list.html", context)
    #return JsonResponse({'data': data, 'cart': cart_json})

                #product_id = str(request.GET['id'])
                # if 'cart_data-obj' in request.session:
                #    if product_id in request.session['cart_data_obj']:
                #        cart_data = request.session['cart_data_obj']
                #        del request.session['cart_data_obj']['product_id']
                #        request.session['cart_data_obj'] = cart_data

                #    cart_total_amount = 0
                #    if 'cart_data_obj' in request.session:
                #        for product_id, item in request.session['cart_data_obj'].items():
                #            cart_total_amount += int(item['qty']) * float(item['price'])

                #    context = render_to_string("async/cart-list.html", {"cart_data": request.session['cart_data_obj'], "totalcartitems": len(
                #        request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
                # return JsonResponse({"data": context, "totalcartitems": len(request.session['cart_data_obj'])})
                # return JsonResponse({"data": context, "totalcartitems": len(cart.num_of_items)})


def update_cart_item(request):
    cart = Cart.objects.all()
    num_of_items = cartitems = cart.cartitems.all()
    totalcartitems = num_of_items

    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    if 'cart_data-obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data(str(request.GET['id']))['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

        cart_total_amount = 0
        if 'cart_data_obj' in request.session:
            for product_id, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['qty']) * float(item['price'])

        context = render_to_string("storeapp/async/cart-list.html", {"cart_data": request.session['cart_data_obj'], "totalcartitems": len(
            request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    # return JsonResponse({"data": context, "totalcartitems": len(request.session['cart_data_obj'])})
    return JsonResponse({"data": context, "totalcartitems": len(cart.num_of_items)})


def payment_completed(request):
    #cart = Cart.objects.get(session_id=request.session['nonuser'], completed=False)
    #cartitems = cart.cartitems.all()

    cartitems = 0
    order = None

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user, completed=False)
        cartitems = cart.cartitems.all()
        order = Cart.objects.filter(user=request.user).order_by("-id")

    else:
        cart = Cart.objects.get(
            session_id=request.session['nonuser'], completed=False)
        if cartitems:
            cartitems = cart.cartitems.all()

        else:
            cart = Cart.objects.get(
                session_id=request.session['nonuser'], completed=False)
            cartitems = cart.cartitems.all()

    context = {
        'cart': cart,
        'cartitems': cartitems,
        'order': order,
    }
    return render(request, "payment-completed.html", context)


def payment_failed(request):
    return render(request, "payment-failed.html")



def about(request):
    # cart, created = Cart.objects.get_or_create(user=request.user, completed=False)  # GET OR CREATE CART FOR LOGGED IN USER
    # GET ALL THE CART ATTRIBUTES FROM THE (CART-ITEM OBJECT LINKED TO CART CLASS THROUGH RELATED-NAME) AND NOT FROM CART'S OBJECT
    context = {
        # "cartitems": cartitems,
        # "cart": cart
    }
    return render(request, 'about.html', context)


def contact(request):
    return render(request, "contact.html")


def ajax_contact_form(request):
    # USING JAVASCRIPT FORMAT
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = ContactUs.objects.create(
        full_name = full_name,
        email = email,
        phone = phone,
        subject = subject,
        message = message
    )

    data = {
        "bool":True,
        "message": "Message sent successfully..."
    }

    return JsonResponse({"data":data})



def services(request):
    # GET ALL THE CART ATTRIBUTES FROM THE (CART-ITEM OBJECT LINKED TO CART CLASS THROUGH RELATED-NAME) AND NOT FROM CART'S OBJECT
    #cartitems = cart.cartitems.all()
    context = {
        # "cartitems": cartitems,
    }
    return render(request, "services.html", context)


def vendor_list(request):
    vendors = Vendor.objects.all()
    # cart, created = Cart.objects.get_or_create(user=request.user, completed=False)  # GET OR CREATE CART FOR LOGGED IN USER
    # GET ALL THE CART ATTRIBUTES FROM THE (CART-ITEM OBJECT LINKED TO CART CLASS THROUGH RELATED-NAME) AND NOT FROM CART'S OBJECT
    #cartitems = cart.cartitems.all()
    if 'search' in request.GET:
        search = request.GET['search']
        # products = Product.objects.filter(name__icontains=search)
        multiple_queries = Q(Q(name__icontains=search) |
                             Q(title__icontains=search))
        vendors = Vendor.objects.filter(multiple_queries)
    else:
        vendors = Vendor.objects.all()
    context = {
        "vendors": vendors,
        # "cart": cart,
        # "cartitems": cartitems
    }
    return render(request, "vendor_list.html", context)

def vendor_delete(request, id):
    vendor = get_object_or_404(Vendor, id=id, user=request.user)
    vendor.delete()
    return redirect("storeapp:vendors")


def vendor_detail(request, id):
    vendor = Vendor.objects.get(id=id)


    #validating vendors for editing and deleting their respective accts
    #vendor_name = vendor.user
    products = Product.objects.filter(vendor=vendor,vendor_product="True")
    # products = Product.objects.filter(vendor=vendor)
    # cart, created = Cart.objects.get_or_create(user=request.user, completed=False)  # GET OR CREATE CART FOR LOGGED IN USER
    # GET ALL THE CART ATTRIBUTES FROM THE (CART-ITEM OBJECT LINKED TO CART CLASS THROUGH RELATED-NAME) AND NOT FROM CART'S OBJECT
    #cartitems = cart.cartitems.all()
    categories = Category.objects.filter(vendor_display="True")

    context = {
        "vendor": vendor,
        #"is_vendor":is_vendor,
        "products": products,
        # "cartitems": cartitems,
        "categories": categories
    }
    return render(request, "vendor-detail.html", context)


def vendor_main_detail(request, id):
    item = Product.objects.get(id=id)
    product = Product.objects.get(name=item)

    categories = Category.objects.filter(vendor_display="True")

    #TO GET 3 RELATED PRODUCTS 
    related_products = Product.objects.filter(category=product.category, vendor_product="True").exclude(id=id)[0:3]

    
    
    context = {
        "categories":categories,
        "product":product,
        "related_products":related_products,
    }
    return render(request, "vendor-main-detail.html", context)

def vendor_product_delete(request, id):
    product = get_object_or_404(Product, id=id, vendor_product="True")
    product.delete()
    return redirect("storeapp:vendors")


@login_required
def new_product(request):
    if request.method == "POST":
        form = VendorNewItemForm(request.POST, request.FILES or None)

        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, f"Hey {request.user} your products were successfully added")
            return redirect("storeapp:vendors")

    else:
        form = VendorNewItemForm()

    context = {
        "form":form
    }

    return render(request, "new_product.html", context)


# VENDOR MODIFY PRODUCT 
def edit_vendor_product(request, id):
    product = get_object_or_404(Product, id=id, created_by=request.user)



    if request.method == "POST":
        form = EditProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()

            return redirect('storeapp:product-detail', id=product.id)
    else:
        form = EditProductForm(instance=product)
    context = {
        "form":form,
    }    
    return render(request, "vendor-product-upload.html", context)    


    # AFTER A SUCCESSFUL PAYMENT, IT DISPLAYS THIS VIEW
@login_required
def check_out(request):
    #cart_total_amount = 0
    total_amount = 0
    cart = 0
    order = 0
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user, completed=False)
        cartitems = cart.cartitems.all()
        cart_total_amount = cart.total_price
    else:
        return redirect('userapp:login')

    #2 GETTING THE ORDER OBJECT
    try:
        order = Cart.objects.get(user=request.user, completed=False)

    except:    
        order = Cart.objects.create(
            user=request.user,
            completed=False
            )

    #GETTING COUPON CODE
    if 'c-code' in request.GET:
        c_code = request.GET['c-code']
        messages.warning(request, "Wrong coupon code ☹")
        return redirect('storeapp:check-out')


    #THE BEGINING TO GETTING ITEMS FOR PAYPAL INTEGRATION
    if 'cart_data_obj' in request.session:


        #1 GETTING TOTAL AMOUNT FOR PAYPAL ACCT
        #cart = Cart.objects.get(user=request.user, completed=False)    
        #cart_total_amount = cart.total_price
        #for item in request.session['cart_data_obj'].items():
            #total_amount = Cart.objects.get(
                #user=request.user, 
                #total_price=request.user,
                #completed=False
                #)
        cart = Cart.objects.get(user=request.user, total_price=request.user, completed=False)
        cartitems = cart.cartitems.all()
        cart_total_amount = cart.total_price
        print("THE CART TOTAL AMOUNT IS =====", cart_total_amount)



        #2 GETTING THE ORDER OBJECT
        order = Cart.objects.create(
            user=request.user, 
            total_price=cart_total_amount,
            completed=False
            )
        if order:
            for single_order in order:
                user_order = single_order.id
                print("THE ORDER IS ======", user_order)


        #3 GETTING THE TOTAL AMOUNT FOR THE CART
        cart = Cart.objects.get(user=request.user, completed=False)
        for item in request.session['cart_data_obj'].items():
            cart_total_amount = cart.total_price

            #Create an Order Object
            cart_order_products = CartItem.objects.create(
                #cart is the order
                cart=order,

                #order.id is the id of order at (#2)
                invoice_no="INVOICE_NO-" + str(user_order),  # GET INVOICE NO
                product=item['product'],
                quantity=item['quantity'],
                price=item['price'],
                #total = float(item.total_price)
            )

            #To create a total price instance
            cart_order_products = Cart.objects.create(
                total_price = float(item.total_price)
            )

            #To create a product image instance
            cart_order_products = Product.objects.create(
                picture = item['image']
            )

    #THE ACTUAL PAYPAL INTEGRATION PROCESS
    host = request.get_host()
    paypal_dict = {
        'business': 'ecommerceprj/settings.PAYPAL_RECEIVER_EMAIL',
        'amount': cart_total_amount,
        'item_name': 'Order-Item-No-' + str(order.id),
        'invoice': "INV_NO-" + str(order.id),
        'Currency_code': "NGN",
        'notify_url': 'http://{}{}'.format(host, reverse("storeapp:paypal-ipn")),
        'return_url': 'http://{}{}'.format(host, reverse("storeapp:payment_completed")),
        'cancel_url': 'http://{}{}'.format(host, reverse("storeapp:payment_failed")),
    }

    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    cartitems = 0

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user, completed=False)
        cartitems = cart.cartitems.all()

    else:
        cart = Cart.objects.get(
            session_id=request.session['nonuser'], completed=False)
        if cartitems:
            cartitems = cart.cartitems.all()
        else:
            cart = Cart.objects.get(
                session_id=request.session['nonuser'], completed=False)
            cartitems = cart.cartitems.all()

    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except:
        messages.warning(
            request, "There are multiple addresses, only one should be activated. ")
        active_address = None

    context = {
        'cart': cart,
        'cartitems': cartitems,
        'paypal_payment_button': paypal_payment_button,
        'active_address':active_address
    }
    return render(request, "check-out.html", context)



# SAVE CHECK-OUT USER INFORMATION
@login_required
def save_checkout_view(request):
    cart_total_amount = 0
    total = 0
    
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        
        request.session['full_name'] = full_name
        request.session['email'] = email
        request.session['mobile'] = mobile
        request.session['address'] = address
        request.session['city'] = city
        request.session['state'] = state
        request.session['country'] = country
        
        if 'cart_data_obj' in request.session:
            for p_id, item in request.session['cart_data_obj'].items():
                total_amount += int(item['qty']) * float(item['price'])
                
                order = CartOrder.objects.create(
                    user = request.user,
                    price = total_amount
                )
                
                for p_id, item in request.session['cart_data_obj'].items():
                    cart_total += int(item['qty']) * float(item['price'])
                    
                    cart_order_products = CartItem.objects.create(
                        order=order,
                        invoice_no="INVOICE_NO-" + str(order.id),  # GET INVOICE NO
                        item=item['title'],
                        image=item['image'],
                        quantity=item['quantity'],
                        price=item['price'],
                        total = float(item['qty']) * float(item['price'])
                    )
                    
                    del request.session['full_name']
                    del request.session['email']
                    del request.session['mobile']
                    del request.session['address']
                    del request.session['city']
                    del request.session['state']
                    del request.session['country']
                    
                    for p_id, item in request.session['cart_data_obj'].items():
                        cart_total_amount += int(item['qty']) * float(item['price'])
                        
                        cart_order_products = CartItem.objects.create(
                            order=order,
                            invoice_no="INVOICE_NO-" + str(order.id),  # GET INVOICE NO
                            item=item['title'],
                            image=item['image'],
                            quantity=item['quantity'],
                            price=item['price'],
                            total = float(item['qty']) * float(item['price'])
                        )
                        cart_order_products.save()
                    
        return redirect('storeapp:check-out')
    return redirect('storeapp:check-out')
                                
                    
                    
        




def confirm_payment(request, pk):
    # pk to get individual cart identified by id
    cart = Cart.objects.get(id=pk)
    cart.completed = True  # once payments been done
    cart.save()
    messages.success(request, "Payment made successfully")
    return redirect('storeapp:home')
