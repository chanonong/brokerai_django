from django.db import models

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
	nn_daily = models.DecimalField(max_digits=15, decimal_places=10)
	nn_weekly = models.DecimalField(max_digits=15, decimal_places=10)
	nn_monthly = models.DecimalField(max_digits=15, decimal_places=10)
	bs_daily = models.DecimalField(max_digits=15, decimal_places=10)
	bs_weekly = models.DecimalField(max_digits=15, decimal_places=10)
	bs_monthly = models.DecimalField(max_digits=15, decimal_places=10)
	dt_daily = models.IntegerField()
	dt_weekly = models.IntegerField()
	dt_monthly = models.IntegerField()

	def __str__(self):
		return self.stock_id

class Users(models.Model):
	first_name = models.CharField(max_length=50)
	surname = models.CharField(max_length=50)
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	email = models.CharField(max_length=50)

	def __str__(self):
		return self.username

class User_favorite(models.Model):
	user_id = models.ForeignKey(Users)
	company_id = models.ForeignKey(Companies)

	def __str__(self):
		return self.user_id.id + " " + self.company_id