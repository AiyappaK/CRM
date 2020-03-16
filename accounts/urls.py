from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('product/',views.product,name="product" ),
    path('customer/<str:pk_test>/',views.Customer,name="customer"),

    path('create_order/<str:pk>/', views.create_order, name = "create_order"),
    path('updateOrder/<str:pk>/', views.updateOrder, name = "updateOrder"),
    path('deleteOrder/<str:pk>/', views.deleteOrder, name = "deleteOrder"),
    path('register/',views.register,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutuser,name='logout'),
    path('user/',views.userPage,name='user'),
    path('account/',views.accountSettings,name="account"),
]
