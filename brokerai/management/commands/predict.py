from django.core.management.base import BaseCommand, CommandError
from brokerai.models import *
from brokerai.serializers import *

class Command(BaseCommand):
	help = 'Import predited data'

	def add_arguments(self, parser):
		parser.add_argument('filename', nargs='+', type=str)

	def handle(self, *args, **options):
		filename = options.get("filename")
		self.stdout.write(str(filename),ending='\n')
		with open(filename[0],'r') as f:
			lines = filter(None,list(map(str.strip,f.readlines())))
			settings = {}
			for line in lines:
				if line.startswith('@'):
					tmp = line[1:].split('=')
					settings[tmp[0]] = tmp[1]
				else:
					try:
						symbol,value = line.split(',')
						#print(symbol,value)

						c = Companies.objects.filter(symbol=symbol)	
						s = Stock_data.objects.filter(company_id=c,date=settings.get('date'))
						#print(s)
						if(len(s) > 0):
							chk = Predicted_data.objects.filter(stock_id=s[0])
							if len(chk) is 0:
								print(s[0])
								chk = Predicted_data(stock_id=s[0])
								print("created")
								chk.save()
							else:
								chk = chk[0]
							print("saved")
							if settings.get('model') == 'nn' and settings.get('type') == 'day':
								Predicted_data.objects.filter(id=chk.id).update(nn_daily=value)
							if settings.get('model') == 'nn' and settings.get('type') == 'week':
								Predicted_data.objects.filter(id=chk.id).update(nn_weekly=value)
							if settings.get('model') == 'nn' and settings.get('type') == 'month':
								Predicted_data.objects.filter(id=chk.id).update(nn_monthly=value)
							if settings.get('model') == 'dt' and settings.get('type') == 'day':
								Predicted_data.objects.filter(id=chk.id).update(dt_daily=value)
							if settings.get('model') == 'dt' and settings.get('type') == 'week':
								Predicted_data.objects.filter(id=chk.id).update(dt_weekly=value)
							if settings.get('model') == 'dt' and settings.get('type') == 'month':
								Predicted_data.objects.filter(id=chk.id).update(dt_monthly=value)
							if settings.get('model') == 'bs' and settings.get('type') == 'day':
								sell,buy,recommend = value.split(':')	
								pd = Predicted_data.objects.filter(id=chk.id).update(bs_daily_buy=buy,bs_daily_sell=sell,bs_daily_recommend=recommend)
							if settings.get('model') == 'bs' and settings.get('type') == 'week':
								sell,buy,recommend = value.split(':')
								Predicted_data.objects.filter(id=chk.id).update(bs_weekly_buy=buy,bs_weekly_sell=sell,bs_weekly_recommend=recommend)
							if settings.get('model') == 'bs' and settings.get('type') == 'month':
								sell,buy,recommend = value.split(':')
								Predicted_data.objects.filter(id=chk.id).update(bs_monthly_buy=buy,bs_monthly_sell=sell,bs_monthly_recommend=recommend)
						else:
							print("no data on this day")
					except:
						pass
			#print(lines)
		#self.stdout.write(str(Companies.objects.all()),ending="\n")

