from django.shortcuts import render
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from API.models import Product, Category, Review, Cart, CartItem
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from API.filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
# A SINGLE FUNCTION FROM OUR "MODELVIEWSET" WE IMPORT BELOW
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
# (ctrl + click TO SELECT A SPECIFIC FUNCTION)
from rest_framework.viewsets import ModelViewSet, GenericViewSet


from userapp.models import Profile, User
from .serializers import UserSerializer, MyTokenObtainPairSerializer, RegisterSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Create your views here.

# USING CLASS BASED VIEW FOR TOKEN-PAIR VIEW(ACCESS AND REFRESH TOKEN)
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



# USING CLASS BASED VIEW FOR REGISTER VIEW
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer


# GET ALL ROUTES

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/'
    ]
    return Response(routes)


# VIEW ONLY FOR AUTHENTICATED USERS
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulations {request.user}, your API just responded to a GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = f"You are doing well"
        data = f'Congratulations {request.user}, your API just responded to a POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)


# USING FUNCTION BASED VIEW FOR DASHBOARD VIEW
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    if request.method == "GET":
        context = f"Hey {request.user}, You are seeing a GET response"
        return Response({'response': context}, status=status.HTTP_200_OK)
    elif request.method == "POST":
        text = request.POST.get("text")
        response = f"Hey {request.user}, your text is {text}"
        return Response({"response": context}, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)







###### ECOMMERCE VIEWS #######

# HANDLES LIST AND DETAIL VIEW
@permission_classes([IsAuthenticated])
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'price', 'title']
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price']  # sort in ascending order by price
    pagination_class = PageNumberPagination  # imported module for pagination

@permission_classes([IsAuthenticated])
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # filter to get "PRODUCT ID" equals its "PRIMARY KEY", this is the method, when using these kinda views
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    # TO PASS THIS CONTEXT TO OUR REVIEWSERIALIZER
    def get_serializer_context(self):
        # JUST SIMILAR TO PASSING CONTEXT TO HTML
        return {'product_id': self.kwargs['product_pk']}


# A SINGLE FUNCTION FROM OUR "MODELVIEWSET" WE IMPORT BELOW "CREATEMODELMIXIN" AND "GENERICVIEWSET"
@permission_classes([IsAuthenticated])
class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

@permission_classes([IsAuthenticated])
class CartItemViewSet(ModelViewSet):

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs["cart_pk"])

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer

        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer

        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}


# CLASS BASED GENERIC VIEWS
# class APIProducts(ListCreateAPIView):
#    queryset = Product.objects.all()
#    serializer_class = ProductSerializer

# DETAIL VIEW
# class APIProduct(RetrieveUpdateDestroyAPIView):
#   queryset = Product.objects.all()
#   serializer_class = ProductSerializer


# @api_view                                 #GET AND POST USING API DECORATORS
# def productlist(request):
#    if request.method == "GET":
#        products = Product. objects.all()
#        serializer = ProductSerializer(products, many=True)
#        return Response(serializer.data)

#    if request.method == "POST":
#        product = get_object_or_404(Product, data = request.data)
#        serializer = ProductSerializer(product)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        else:
#            return Response(serializer.errors)

# GET, PUT AND DELETE USING API DECORATORS
# @api_view
# def productdetail(request):  # GET, PUT , DELETE
#    product = get_object_or_404(Product, data=request.data)
#    if request.method == "GET":
#        products = Product. objects.all()
#        serializer = ProductSerializer(products, many=True)
#        return Response(serializer.data)

#    if request.method == "PUT":
#        serializer = ProductSerializer(product)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_200_OK)
#        else:
#            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

#    if request.method == "DELETE":
#        serializer.delete()
#        return Response(status=status.HTTP_404_VALID)
