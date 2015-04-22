from django.conf.urls import url

from rest_framework import serializers

from rest_framework import routers
from brokerai import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^forlearn', views.forLearn, name='forLearn'),
    # Companies
	url(r'^companies/', views.companies_list, name='companies_list'),
	# Stock Data
	url(r'^stocks/', views.stock_data, name='stock_data'),
	# Predicted Data
	url(r'^predicted/', views.predicted_data, name='predicted_data'),
	# Users
	url(r'^users/', views.users, name='users'),
	# User Favorite
	url(r'^favorite/', views.user_favorite, name='user_favorite'),
]