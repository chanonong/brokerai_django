from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import serializers

from rest_framework import routers
from brokerai import views

router = routers.DefaultRouter()

urlpatterns = [
    # Examples:
    # url(r'^$', 'brokerai_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	# url(r'^$', include('brokerai.urls')),
	url(r'^api/', include('brokerai.urls')),
	url(r'^initCompanies/', views.initCompanies, name='initCompanies'),
	# url(r'^initStocks/', views.initStocks, name='initStocks'),
	url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
