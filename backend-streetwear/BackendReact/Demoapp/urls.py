from django.urls import path

from Demoapp import views


urlpatterns = [
    path('nike/', views.NikeList.as_view()),
    path('nike/<int:pk>/', views.NikeDetails.as_view()),
    path('register/', views.UserRegistrationView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('logout/', views.UserLogoutView.as_view()),
]

