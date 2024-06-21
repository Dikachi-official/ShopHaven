from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers  # has "DefaultRouter" attribute
from rest_framework_simplejwt.views import TokenRefreshView


app_name = 'api'



router = DefaultRouter()
router.register('products', views.ProductViewSet)  # PRODUCT PARENT ROUTER
router.register('carts', views.CartViewSet)  # CART PARENT ROUTER
product_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
# Register our variable
product_router.register('reviews', views.ReviewViewSet,
                        basename='product-reviews')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup="cart")
cart_router.register("items", views.CartItemViewSet, basename="cart-items")



urlpatterns = [

    # REFRESH AND ACCESS TOKEN URL
    path('token/', views.MyTokenObtainPairView.as_view()),

    # REFRESH TOKEN URL
    path('token/refresh/', TokenRefreshView.as_view()),

    # REGISTER URL PAGE
    path('register/', views.RegisterView.as_view()),

    # DASHBOARD URL PAGE
    path('dashboard/', views.dashboard),

    # TEST URL PAGE
    path('test/', views.testEndPoint, name='test'),

    # TO DISPLAY ALL THE ROUTES IN OUR API
    path('', views.getRoutes),



    ##### ECOMMERCE URL ######
    # URL ENDPOINT:localhost/api/product/id
    path('', include(router.urls)),

    # URL ENDPOINT:localhost/api/products/id/reviews
    path('', include(product_router.urls)),

    # URL ENDPOINT:localhost/api/cart/uuid/items
    path('', include(cart_router.urls))








    #path('products', views.APIProducts.as_view()),
    # URL ENDPOINT:localhost/api/product/id
    #path('product/<str:pk>', views.APIProduct.as_view())
]
