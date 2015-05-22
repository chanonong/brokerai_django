from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Companies(models.Model):
	name = models.CharField(max_length=50)
	symbol = models.CharField(max_length=50)
	
	def __str__(self):
		return self.name

class Stock_data(models.Model):
	company_id = models.ForeignKey(Companies)
	open_price = models.DecimalField(max_digits=15, decimal_places=10)
	low_price = models.DecimalField(max_digits=15, decimal_places=10)
	high_price = models.DecimalField(max_digits=15, decimal_places=10)
	close_price = models.DecimalField(max_digits=15, decimal_places=10)
	volume = models.IntegerField()#.DecimalField(max_digits=15, decimal_places=10)
	date = models.DateField()
	currency = models.CharField(max_length=10)

	def __str__(self):
		return self.company_id.symbol + " " + str(self.date)

class Predicted_data(models.Model):
	stock_id = models.ForeignKey(Stock_data)
	nn_daily = models.DecimalField(max_digits=15, decimal_places=10,null=True)
	nn_weekly = models.DecimalField(max_digits=15, decimal_places=10,null=True)
	nn_monthly = models.DecimalField(max_digits=15, decimal_places=10,null=True)
	bs_daily_buy = models.DecimalField(max_digits=15, decimal_places=10,null=True)
	bs_daily_sell = models.DecimalField(max_digits=15, decimal_places=10,null=True)
	bs_daily_recommend = models.BooleanField(default=True)
	bs_weekly_buy = models.DecimalField(max_digits=15, decimal_places=10,null=True)
	bs_weekly_sell = models.DecimalField(max_digits=15, decimal_places=10,null=True)
	bs_weekly_recommend = models.BooleanField(default=True)
	bs_monthly_buy = models.DecimalField(max_digits=15, decimal_places=10,null=True)
	bs_monthly_sell = models.DecimalField(max_digits=15, decimal_places=10,null=True)
	bs_monthly_recommend = models.BooleanField(default=True)
	dt_daily = models.DecimalField(max_digits=15, decimal_places=10,null=True)
	dt_weekly = models.DecimalField(max_digits=15, decimal_places=10,null=True)
	dt_monthly = models.DecimalField(max_digits=15, decimal_places=10,null=True)

	def __str__(self):
		return str(self.stock_id)

class Users(models.Model):
	first_name = models.CharField(max_length=50)
	surname = models.CharField(max_length=50)
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	email = models.CharField(max_length=50)

	def __str__(self):
		return self.username

class User_favorite(models.Model):
	user_id = models.ForeignKey(User)
	company_id = models.ForeignKey(Companies)
	
	class Meta:
		unique_together = ('user_id', 'company_id')

	def __str__(self):
		return str(self.user_id) + " --> " + str(self.company_id)
