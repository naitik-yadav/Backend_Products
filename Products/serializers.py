from rest_framework import serializers
from Products.models import CustomUser, Products, Cart, CartItem, Order, OrderItem
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'contact_number', 'role', 'is_active', 'is_staff']
        read_only_fields = ['id','is_active', 'is_staff']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES, default='user')

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'contact_number', 'password', 'role']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            contact_number=validated_data['contact_number'],
            role=validated_data.get('role', 'user')
        )
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not (email and password):
            raise serializers.ValidationError("Both email and password are required.")
        
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        
        return data


class LogoutSerializer(serializers.Serializer):
    pass


class ProductSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Products
        fields = ['id', 'product_name', 'product_number', 'product_type', 'description', 'category', 'Price', 'images']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = self.context['request'].user
        product = Products.objects.create(user=user, **validated_data)
        return product    

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer() 
    cart = serializers.StringRelatedField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'created_at', 'updated_at']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'cart', 'order_status', 'created_at', 'updated_at']

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    order = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'created_at', 'updated_at']

class CartItemListSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at', 'updated_at']

class OrderItemListSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'order_status', 'created_at', 'updated_at']
