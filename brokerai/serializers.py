from django.contrib.auth.models import User, Group
from rest_framework import serializers
from brokerai.models import *


class CompaniesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Companies
		fields = ('id', 'name', 'symbol')

class StockDataSerializer(serializers.ModelSerializer):
	company_id = serializers.PrimaryKeyRelatedField(read_only=True)
	class Meta:
		model = Stock_data
		fields = ('id', 'company_id', 'open_price', 'low_price', 'high_price', 'close_price', 'volume', 'date', 'currency')

class PredictedDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = Predicted_data
		fields = ('id', 'stock_id', 'nn_daily', 'nn_weekly', 'nn_monthly', 'dt_daily', 'dt_weekly', 'dt_monthly', 'bs_daily_buy', 'bs_daily_sell', 'bs_daily_recommend', 'bs_weekly_buy', 'bs_weekly_sell','bs_weekly_recommend','bs_monthly_buy','bs_monthly_sell','bs_monthly_recommend')

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

	def update(self, instance, validated_data):
	    instance.first_name = validated_data.get('first_name', instance.first_name)
	    instance.surname = validated_data.get('last_name', instance.surname)
	    instance.username = validated_data.get('username', instance.username)
	    instance.password = validated_data.get('password', instance.password)
	    instance.email = validated_data.get('email', instance.email)
	    instance.save()
	    return instance

	def create(self, validated_data):
		user = User.objects.create(
		username=validated_data['username']
		)
		user.set_password(validated_data['password'])
		user.save()
		return user
			

class UserFavoriteSerializer(serializers.ModelSerializer):
	class Meta:
		model = User_favorite
		fields = ('id', 'user_id', 'company_id')

