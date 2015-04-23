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

class UsersSerializer(serializers.ModelSerializer):
	class Meta:
		model = Users
		fields = ('id', 'first_name', 'surname', 'username', 'password', 'email')
		extra_kwargs = {'password' : {'write_only':True}}

	def update(self, instance, validated_data):
	    instance.first_name = validated_data.get('first_name', instance.first_name)
	    instance.surname = validated_data.get('surname', instance.surname)
	    instance.username = validated_data.get('username', instance.username)
	    instance.password = validated_data.get('password', instance.password)
	    instance.email = validated_data.get('email', instance.email)
	    instance.style = validated_data.get('style', instance.style)
	    instance.save()
	    return instance

	def create(self, validated_data):
	    return Users.objects.create(**validated_data)

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'first_name', 'last_name', 'username', 'password', 'email')
		extra_kwargs = {'password' : {'write_only':True}}
			

class UserFavoriteSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User_favorite
		fields = ('id', 'user_id', 'company_id')
