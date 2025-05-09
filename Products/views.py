from rest_framework.response import Response
from rest_framework import status
from Products.models import CustomUser, Products, Cart, CartItem, Order, OrderItem
from Products.serializers import UserSerializer, RegisterSerializer, LoginSerializer, LogoutSerializer, ProductSerializer, CartSerializer, CartItemSerializer, CartItemListSerializer, OrderSerializer, OrderItemSerializer, OrderItemListSerializer
from utils.base_views import BaseGenericAPIView
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

class RegisterView(BaseGenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class LoginView(BaseGenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(request, email=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                }, status=status.HTTP_200_OK)
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(BaseGenericAPIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:  
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserView(BaseGenericAPIView):
    # permission_classes = [permissions.IsAuthenticated]

    serializer_class = UserSerializer

    def get(self, request):
        user = CustomUser.objects.all()
        serializer = self.get_serializer(user, many=True)
        return Response(serializer.data)
    
class UserRetriveUpdateDeleteView(BaseGenericAPIView):
    # permission_classes = [permissions.IsAuthenticated]

    serializer_class = UserSerializer

    def get_object(self, pk):
        return get_object_or_404(CustomUser, pk=pk)

    def get(self, request, pk):
        """
          Get api for user retrieve using id
        """
        user = self.get_object(pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        """
           Put api for user update
        """
        user = self.get_object(pk)
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
           Patch api for user
        """
        user = self.get_object(pk)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
           Delete api for user
        """
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductView(BaseGenericAPIView):
    # permission_classes = [permissions.IsAuthenticated]

    serializer_class = ProductSerializer

    def get(self, request):
        products = Products.objects.all()
        for product in products:
            if product.image:
                product.image = cloudinary.CloudinaryImage(product.image).build_url()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

class ProductRetrieveUpdateDeleteView(BaseGenericAPIView):
    # permission_classes = [permissions.IsAuthenticated]

    serializer_class = ProductSerializer

    def get_object(self, pk):
        return get_object_or_404(Products, pk=pk)

    def get(self, request, pk):
        """
          Get api for product retrieve using id
        """
        product = self.get_object(pk)
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        """
           Put api for product update
        """
        product = self.get_object(pk)
        serializer = self.get_serializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
           Patch api for product
        """
        product = self.get_object(pk)
        serializer = self.get_serializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
           Delete api for product
        """
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CreateProductView(BaseGenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CartAPI(BaseGenericAPIView):

    def get_cart(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart

    def get(self, request):
        cart = self.get_cart(request)
        serializer = CartItemListSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        cart = self.get_cart(request)
        product_id = request.data.get('product_id')
        product = get_object_or_404(Products, pk=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        serializer = CartItemListSerializer(cart)
        return Response(serializer.data)

class CartItemAPI(BaseGenericAPIView):

    def get_cart_item(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk)
        return cart_item

    def delete(self, request, pk):
        cart_item = self.get_cart_item(request, pk)
        cart_item.delete()
        serializer = CartItemListSerializer(cart_item.cart)
        return Response(serializer.data)

    def patch(self, request, pk):
        cart_item = self.get_cart_item(request, pk)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderAPI(BaseGenericAPIView):

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        order = Order.objects.create(user=request.user, cart=cart)
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
            cart_item.delete()
        serializer = OrderItemListSerializer(order)
        return Response(serializer.data)


class OrderDetailAPI(BaseGenericAPIView):

    def get_order(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        return order

    def get(self, request, pk):
        order = self.get_order(request, pk)
        serializer = OrderItemListSerializer(order)
        return Response(serializer.data)

class OrderListAPI(BaseGenericAPIView):

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderItemListSerializer(orders, many=True)
        return Response(serializer.data)    