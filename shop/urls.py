
app_name = 'shop'
from django.contrib import admin
from django.urls import path,include
# from django.contrib.auth import views as auth_view
from .views import registerPage,index,employee,products,OrderView,loginPage,logoutUser,product_delete,product_detail,product_edit,employee,employee_detail,ItemDetailView

urlpatterns = [
    path('', index, name='shop-index'),
    path('products/', products, name='dashboard-products'),
    path('employees/', employee, name='shop-employee'),
    path('products/delete/<int:pk>/', product_delete,
         name='dashboard-products-delete'),
    path('products/detail/<int:pk>/', product_detail,
         name='dashboard-products-detail'),
    path('products/edit/<int:pk>/', product_edit,
         name='dashboard-products-edit'),
    path('order/<pk>/', ItemDetailView.as_view(), name='order_view'),
    path('employee/detial/<int:pk>/', employee_detail,
         name='dashboard-customer-detail'),
    path('order/',OrderView.as_view(), name='dashboard-order'),
    path('login/', loginPage, name='account_login'),
    path('signup/', registerPage, name='account_signup'),
    path('logout/', logoutUser, name='account_logout'),
    # path('login/', auth_view.LoginView.as_view(), name='account_login'),
    # path('logout/', auth_view.LogoutView.as_view(), name='account_logout'),
]