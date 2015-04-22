from django.contrib import admin
from brokerai.models import Companies, Stock_data, Predicted_data, Users, User_favorite
# Register your models here.

class CompaniesAdmin(admin.ModelAdmin):
	fields = ['name', 'symbol']

class StockDataAdmin(admin.ModelAdmin):
	fields = ['company_id','open_price','high_price','low_price','close_price','volume','date','currency']

class PredictedDataAdmin(admin.ModelAdmin):
	fields = ['stock_id', 'nn_daily', 'nn_weekly', 'nn_monthly', 'dt_daily', 'dt_weekly', 'dt_monthly', 'bs_daily', 'bs_weekly', 'bs_monthly']

class UsersAdmin(admin.ModelAdmin):
	fields = ['first_name', 'surname', 'username', 'password', 'email']

class UserFavoriteAdmin(admin.ModelAdmin):
	fields = ['user_id', 'company_id']

admin.site.register(Companies, CompaniesAdmin)
admin.site.register(Stock_data,StockDataAdmin)
admin.site.register(Predicted_data)
admin.site.register(Users)
admin.site.register(User_favorite)

