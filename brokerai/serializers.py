from django.contrib.auth.models import User, Group
from rest_framework import serializers
from brokerai.models import *


class CompaniesSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Companies
		fields = ('id', 'name', 'symbol')

class StockDataSerializer(serializers.ModelSerializer):
	company_id = serializers.PrimaryKeyRelatedField(read_only=True)
	class Meta:
		model = Stock_data
		fields = ('id', 'company_id', 'open_price', 'low_price', 'high_price', 'close_price', 'volume', 'date', 'currency')

class PredictedDataSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Predicted_data
		fields = ('id', 'stock_id', 'nn_daily', 'nn_weekly', 'nn_monthly', 'dt_daily', 'dt_weekly', 'dt_monthly', 'bs_daily', 'bs_weekly', 'bs_monthly')

class UsersSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Users
		fields = ('id', 'first_name', 'surname', 'username', 'password', 'email')

class UserFavoriteSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User_favorite
		fields = ('id', 'user_id', 'company_id')
