from .views import HomeView, registerPage, loginPage, logoutUser, OrderSummaryView, CatView, CheckoutView, aboutus, Author, ItemDetailView, add_to_cart, AddCouponView, remove_from_cart, remove_single_item_from_cart, RequestRefundView,subCatView,search,order_history,profileView,wishList,add_to_wishlist
# ,forgot_password,reset_password
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
app_name = 'user'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('register/', registerPage, name="register"),
    path('search/', search, name="search"),
    path('User_Profile/<pk>', profileView, name="profile"),
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),
    path('category/<slug>', CatView.as_view(), name='category'),
    path('subcategory/<slug>', subCatView.as_view(), name='subcategory'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('aboutus/', aboutus, name='aboutus'),
    path('aboutus/<slug>', Author.as_view(), name='author'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    # path('payment/<payment_option>/', payment_online, name='payment'),
    # path("payment/process/", process_payment, name="process_payment"),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('order-history/<pk>/', order_history, name='order-history'), 
    # Wish List
    path("wishlist", wishList, name="wishlist"),
    path("wishlist/add_to_wishlist/<int:id>", add_to_wishlist, name="user_wishlist"),
    # path('forgot-password/', forgot_password, name='forgot_password'),
    # path('reset-password/<str:token>/', reset_password, name='reset_password'),
    # Other URL patterns
    # path('reset-password/', auth_views.PasswordResetView.as_view(template_name='reset_password.html'), name='password_reset'),
    # path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    # path('reset-password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    # path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
