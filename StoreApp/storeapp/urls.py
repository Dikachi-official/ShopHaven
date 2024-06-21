from django.urls import path, include
from . import views


app_name = "storeapp"

urlpatterns = [
    # HOME URL
    path('', views.index, name='home'),

    # PRODUCT URL
    path('product', views.products, name='products'),  # PRODUCT MAIN PAGE
    path('detail/<str:slug>/', views.detail, name='detail'),

    # CATEGORY URL
    path('categories', views.category_list, name="categories"),
    path('category/<id>', views.category_detail, name="category_detail"),

    # WOMEN URL
    path('women', views.women, name='women'),
    path('women/<slug>', views.women_detail, name="women_detail"),

    # GADGET URL
    path('gadgets/', views.gadgets, name='gadgets'),
    path('gadgets/<str:slug>', views.gadgetsdetail, name='gadgetsdetail'),

    # GAME URL
    path('games/', views.games, name='games'),  # GAME MAIN PAGE
    path('gamesdetail/<str:slug>/', views.gamesdetail, name='gamesdetail'),

    # Filter Product URL
    path('filter-product', views.filter_product, name="filter-product"),

    # Add Review
    path('ajax_add_review/<int:id>', views.ajax_add_review, name="ajax_add_review"),

    # Add Likes
    path('review_likes/<str:id>', views.review_likes, name="review_likes"),

    # add tags
    path('products/tag/<slug:tag_slug>/', views.tag_list, name='tags'),

    # About Section URL
    path('about', views.about, name='about'),

    # Services URL
    path('services', views.services, name='services'),

    # Vendor List URL
    path('vendors', views.vendor_list, name='vendors'),

    #Vendor Delete URL
    path('delete-vendor/<str:id>/', views.vendor_delete, name="delete-vendor"),

    # Vendor Detail URL
    path('vendor-detail/<id>', views.vendor_detail, name='vendor-detail'),

    #Vendor product detail
    path('product-detail/<str:id>/', views.vendor_main_detail, name="product-detail"),

    #Vendor edit product page URL
    path('edit-product/<str:id>/', views.edit_vendor_product, name='edit-product'),
    
    # Vendor add new product URL
    path('new-products', views.new_product, name="new-products"),

    #Vendor delete product URL
    path('delete-product/<str:id>/', views.vendor_product_delete, name="delete-product"),

    # DASHBOARD URL
    path('user/dashboard', views.dashboard, name="dashboard"),

    #SETTINGS AND PRIVACY
    path('settings/', views.settings, name="settings"),

    # MAKING DEFAULT ADDRESS URL AT DASHBOARD
    path('make-default-address/', views.make_default_address,
         name="make-default-address"),

    # ORDER DETAIL URL
    path('user/order/<id>', views.order_detail, name="order-detail"),

    #WISHLIST URL
    path('wishlists', views.wishlist, name="wishlists"),

    #ADD TO WISHLIST
    path('add-to-wishlist', views.add_to_wishlist, name="add-to-wishlist"),


    #REMOVE TO WISHLIST
    path('delete-from-wishlist', views.remove_wishlist, name='delete-from-wishlist'),

    # Add to cart URL
    path('add_to_cart', views.add_to_cart, name='add'), 

    # Delete cart item URL
    #path('delete-cart', views.delete_cart_item, name='delete-cart-item'),
    path('delete-item/<id>', views.delete_cartitem_view, name='delete-item'),
    # Update cart URL
    path('update-cart', views.update_cart_item, name='update-cart-item'),

    # Cart URL
    path('cart/', views.cart, name='cart'),

    # Payment completed URL
    path('payment_completed', views.payment_completed, name='payment_completed'),

    # Payment failed
    path('payment_failed', views.payment_failed, name='payment_failed'),

    # Check Out URL
    path("check-out", views.check_out, name="check-out"),
    path("checkout/<str:oid>", views.save_checkout_view, name='checkout_id'),

    # PAYPAL URL
    path('paypal/', include("paypal.standard.ipn.urls")),

    # Payment with flutter URL
    path('confirm_payment/<str:pk>', views.confirm_payment, name='confirm_payment'),

    #CONTACT US URL 
    path('contact/', views.contact, name="contact"),
    path('ajax-contact-form/', views.ajax_contact_form, name="ajax-contact-form"),
]
