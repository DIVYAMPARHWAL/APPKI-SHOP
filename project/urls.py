"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from user.views import aboutus,Author
from django.contrib.auth import views as auth_views
from user.views import MyPasswordResetView , MyPasswordResetDoneView ,MyPasswordResetCompleteView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('delivery/', include('delivery.urls', namespace='delivery')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('sellerpatners/', sellerpatners, name='sellerpatners'),
    path('aboutus/', aboutus, name='aboutus'),
    path('aboutus/<slug>', Author.as_view(), name='author'),
    path('', include('user.urls', namespace='user')),
    path('reset_password/', MyPasswordResetView.as_view(), name='mypasswordresetview'),
    path('reset_password/done/', MyPasswordResetDoneView.as_view(), name='mypasswordresetdoneview'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    ]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)