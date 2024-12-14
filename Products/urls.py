from django.urls import path

from Products import views


urlpatterns = [
    # path('nike/', views.NikeList.as_view()),
    # path('nike/<int:pk>/', views.NikeDetails.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('user/', views.UserView.as_view()),
    path('user/<int:pk>/', views.UserRetriveUpdateDeleteView.as_view(), name='user'),
    path('products/', views.ProductView.as_view()),
    path('products/<int:pk>/', views.ProductRetrieveUpdateDeleteView.as_view()),
    path('create-product/', views.CreateProductView.as_view()),
    path('cart/', views.CartAPI.as_view()),
    path('cart/<int:pk>/', views.CartItemAPI.as_view()),
    path('orders/', views.OrderAPI.as_view()),
    path('orders/<int:pk>/', views.OrderDetailAPI.as_view()),
    path('orders/list/', views.OrderListAPI.as_view()),
]

