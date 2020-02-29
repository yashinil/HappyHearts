"""inventorysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from inventoryapp import views


from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^login/$', views.login_inventory),
    #url(r'^register/$', views.register),
    #url(r'^logout/', views.logout_inventory),
    url(r'^index/', views.index),
    url(r'^about/', views.about),
    url(r'^service/', views.service),
    url(r'^contact/', views.contact),
    url(r'^blogtwo/', views.blog),
    url(r'^portfolio/', views.portfolio),
    url(r'^shortcodes/', views.shortcodes),
    #url(r'^lenderform/$',views.lenderform),
    #url(r'^cart/$',views.cart),
    #url(r'^arrival/$',views.inventorylist),
    #url(r'^inventorylist/$',views.inventorylist),
]



if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


