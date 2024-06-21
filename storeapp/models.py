from django.db import models
from userapp.models import User, Profile
import uuid  # TO USE UUID
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from django.conf import settings
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

STATUS_CHOICE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In review"),
    ("rejected", "Rejected"),
)


RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)


def user_directory_path(instance, filename):
    return 'user_(0)/(1)'.format(instance.user.id, filename)


class Category(models.Model):
    image = models.ImageField(upload_to="img", default="")
    title = models.CharField(max_length=200)
    slug = models.SlugField(default=None)
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True)
    vendor_display = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


# PRODUCTS
# FOR PRODUCTS AND CATEGORY

class Vendor(models.Model):
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path)
    cover_image = models.ImageField(
        upload_to=user_directory_path, blank=True, null=True)
    #description = models.TextField(null=True, blank=True, default="Great vendor at yoyur service")
    description = RichTextUploadingField(null=True, blank=True, default="I am an amazing vendor")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    default = models.BooleanField(default=False)
    address = models.CharField(
        max_length=200, default="Complex 13, ShopRite Ikeja, Off Secretariat Rd, Lagos. Nigeria")
    contact = models.CharField(max_length=100, default="+234 810 4848 223")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=200, default="100")
    days_return = models.CharField(max_length=100, default="50")
    warranty_period = models.CharField(max_length=100, default="100")

    class Meta:
        verbose_name_plural = "Vendors"

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    picture = models.ImageField(upload_to="img", default="")
    slug = models.SlugField(default=None)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    description = models.TextField(null=True, default="This is a quality product")
    #description = RichTextUploadingField(null=True, blank=True, default="Quality product")
    product_status = models.CharField(
        choices=STATUS, max_length=10, default="in_review")
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, null=True, blank=True, related_name="vendor")
    old_price = models.IntegerField(null=True, blank=True)
    address = models.CharField(
        max_length=200, default="Complex 13, ShopRite Ikeja, Off Secretariat Rd, Lagos. Nigeria")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendoruser', null=True)
    tags = TaggableManager(blank=True)

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    vendor_product = models.BooleanField(default=False)
    women = models.BooleanField(default=False)
    gadgets = models.BooleanField(default=False)
    games = models.BooleanField(default=False)

    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name  # TO IDENTIFY CLASS BY NAME

    class Meta:
        ordering = ['-price']

    def get_percentage(self):
        updated_price = (self.old_price - self.price)  / self.old_price  * 100
        return updated_price



# CART
class Cart(models.Model):
    # TO MAKE UUID OUR ID FOR SECURITY
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    # WE MAKE USE OF DJANGO DEFAULT User, HENCE THE FOREIGNKEY IS USE
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)  # IF PAYMENTS BEEN MADE
    session_id = models.CharField(max_length=200, null=True, blank=True)
    created_on = models.DateField(auto_now=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")

    def __str__(self):
        return str(self.id)  # TO IDENTIFY THE CART BY THE ID

    @ property
    def total_price(self):
        # GET ALL ATTRIBUTES OF (CARTITEM, WHICH IS OBJECT CART'S RELATED_NAME BELOW)
        cartitems = self.cartitems.all()
        total = sum([item.price for item in cartitems])
        return total

    @ property
    def num_of_item(self):
        cartitems = self.cartitems.all()
        quantity = sum([item.quantity for item in cartitems])
        return quantity


# CARTITEMS
class CartItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='items')
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cartitems')
    # AMOUNT ON CARTITEM, DEFAULT IS EMPTY COS NOTHING HAS BEEN ADDED
    quantity = models.IntegerField(default=0)
    invoice_no = models.CharField(max_length=200, null=True, blank=True)
    product_status = models.CharField(
        choices=STATUS_CHOICE, max_length=200, default="processing")
    def __str__(self):
        return self.product.name  # TO IDENTIFY THE CART ITEM BY THE PRODUCT NAME

    @ property  # TO DISPLAY PRICE OF INDIVIDUAL ITEMS AT CHECKOUT SECTION
    def price(self):
        new_price = self.product.price * self.quantity
        return new_price
    
    

#####  FOR GUEST USER TO BE ABLE TO CHECK OUT AT CART PAGE
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    saved = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    
    shipping_method = models.CharField(max_length=100, null=True, blank=True)
    tracking_id = models.CharField(max_length=100, null=True, blank=True)
    tracking_website_address = models.CharField(max_length=100, null=True, blank=True)
    
    paid_status = models.BooleanField(default=False, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")
    sku = ShortUUIDField(null=True, blank=True, length=5, prefix="sku", max_length=20, alphabet="abcdefgh12345")
    stripe_payment_intent = models.CharField(max_length=1000, null=True, blank=True)
    order_id = ShortUUIDField(null=True, blank=True, length=5, max_length=20, alphabet="123456789")
    
    class Meta:
        verbose_name_plural = "Cart Order"
    


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="review")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="reviewlikes", blank=True)

    def number_of_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.name

    def get_rating(self):
        return self.rating


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)
    mobile = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.address
    
    class Meta:
        verbose_name_plural = 'Address'


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "wishlists"

    def __str__(self):
        return self.product.name
