from django.conf.urls import url

from rest_framework import serializers

from rest_framework import routers

from brokerai import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # forlearning
    url(r'^forlearn/day/$', views.for_learn_day, name='for_learn_day'),
    url(r'^forlearn/week/$', views.for_learn_week, name='for_learn_week'),
    url(r'^forlearn/month/$', views.for_learn_month, name='for_learn_month'),
    url(r'^forlearn/latest/day/$', views.latest_day, name='latest_day'),
    url(r'^forlearn/latest/week/$', views.latest_week, name='latest_week'),
    url(r'^forlearn/latest/month/$', views.latest_month, name='latest_month'),
    # Companies
	url(r'^companies/$', views.companies_list, name='companies_list'),
	url(r'^companies/(?P<cid>[0-9]+)/$', views.companies_list_id, name='companies_list_id'),
	# Stock Data
	url(r'^stocks/$', views.stock_data, name='stock_data'),
	url(r'^stocks/(?P<cid>[0-9]+)/$', views.stock_data_company_id, name='stock_data_company_id'),
	url(r'^stocks/(?P<symbol>\w+)/$', views.stock_data_company_symbol, name='stock_data_company_symbol'),
	url(r'^lateststocks/$', views.latest_stock, name='latest_stock'),
	url(r'^lateststocks/(?P<cid>[0-9]+)/$', views.latest_stock_company_id, name='latest_stock_company_id'),
	# Predicted Data
	url(r'^predicted/$', views.predicted_data, name='predicted_data'),
	url(r'^predicted/companies/(?P<cid>[0-9]+)/$', views.predicted_data_company_id, name='predicted_data_company_id'),
	# Users
	url(r'^users/$', views.users, name='users'),
	# User Favorite
	url(r'^favorite/$', views.user_favorite, name='user_favorite'),
	# Login
	url(r'^login/$', 'rest_framework_jwt.views.obtain_jwt_token'),
	# Register
	url(r'^register/$', views.register, name='register'),
]
