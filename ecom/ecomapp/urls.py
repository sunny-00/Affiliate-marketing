from django.urls import path
from ecomapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register',views.register,name='register'),
    path('index',views.index),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('home',views.home),
    path('search',views.search),
    path('profile',views.profile),
    path('save',views.save),
    path('details/<id>',views.details),
    path('addcart/<rid>',views.addcart),
    path('cart',views.cart),
    path('remove/<id>',views.remove),
    path('placeorder',views.placeorder),
    path('contact',views.contact),
    path('about',views.about),
    path('promoter',views.promoter),
    path('buyer',views.buyer),
    path('makepayment',views.makepayment),
    path('sendmail',views.sendmail),

    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
