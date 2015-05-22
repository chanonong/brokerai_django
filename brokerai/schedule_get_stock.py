import urllib.request
import urllib.parse
from time import sleep
from brokerai.models import *
from brokerai.serializers import *
from django.db.models import Max,Count
import urllib.request
import urllib.parse
from datetime import datetime
from time import sleep
import json
from operator import itemgetter
import sys
import os

NUMBER_OF_DAYS = 10
HOST = 'http://dev.markitondemand.com'
PATH = '/Api/v2/InteractiveChart/json?parameters='
TMP_FOLDER_PATH = os.path.split(__file__)[0] + '/tmp/'
print(TMP_FOLDER_PATH)
def cleanlog():
	with open(TMP_FOLDER_PATH + 'log.txt','w') as log:
		log.write('')

def log(data):
	with open(TMP_FOLDER_PATH + 'log.txt','a') as log:
		log.write(data)

def extractData(line):
	listOfStock = []
	data_json = json.loads(line)
	_symbol = data_json["Elements"][0]["Symbol"]
	_currency = data_json["Elements"][0]["Currency"]
	_date = data_json["Dates"]
	_open = data_json["Elements"][0]["DataSeries"]["open"]["values"]
	_high = data_json["Elements"][0]["DataSeries"]["high"]["values"]
	_low = data_json["Elements"][0]["DataSeries"]["low"]["values"]
	_close = data_json["Elements"][0]["DataSeries"]["close"]["values"]
	_volume = data_json["Elements"][1]["DataSeries"]["volume"]["values"]
	res = list(zip(_date,_open,_high,_low,_close,_volume))
	stockData = []
	for stock in res:
		tmp = {}
		tmp["symbol"] = _symbol
		tmp["open"] = stock[1]
		tmp["high"] = stock[2]
		tmp["low"] = stock[3]
		tmp["close"] = stock[4]
		tmp["volume"] = stock[5]
		tmp["date"] = stock[0]
		tmp["currency"] = _currency
		stockData += [tmp]
	listOfStock += stockData

	return listOfStock

def cronStock():

	with open(TMP_FOLDER_PATH + 'available_company.txt','r') as f:
		data = f.readlines()
		for i in data:
			try:
				symbol = i.split('\t')[0]
				company = Companies.objects.get(symbol=symbol)
				latest = Stock_data.objects.filter(company_id = company).latest('date')

				params = '{"Normalized":false,"NumberOfDays":"'+ str(NUMBER_OF_DAYS) +'","DataPeriod":"Day","Elements":[{"Symbol":"'+ symbol +'","Type":"price","Params":["ohlc"]},{"Symbol":"'+ symbol +'","Type":"volume","Params":["c"]}]}'
				url = HOST + PATH + urllib.parse.quote(params, safe ='/\"')
				res = urllib.request.urlopen(url)
				res_data = res.read().decode('utf-8')
				#print(res_data)
				extracted = extractData(res_data)
				latest_extracted = sorted(extracted, key = itemgetter('date'))
				for j in latest_extracted:
					if datetime.strptime(j["date"],'%Y-%m-%dT%H:%M:%S').date() > latest.date:
						company = Companies.objects.get(symbol = j["symbol"])
						stock = Stock_data(company_id = company, open_price = j["open"], high_price = j["high"], low_price= j["low"], close_price= j["close"], volume= j["volume"], date = datetime.strptime(j["date"],'%Y-%m-%dT%H:%M:%S') , currency= j["currency"])
						stock.save()
						#stock = Stock_data()
						log('Save '+ symbol + ' ' + str(datetime.strptime(j["date"],'%Y-%m-%dT%H:%M:%S').date()) + ' > ' + str(latest.date) + '\n' )
					else:
						log('Discard '+ symbol + ' ' + str(datetime.strptime(j["date"],'%Y-%m-%dT%H:%M:%S').date()) + ' > ' + str(latest.date) + '\n' )
				sleep(5)
			except Exception:
				log(str(sys.exc_info()[0]) + '\n')
				continue

	# with open(TMP_FOLDER_PATH + 'a.txt','a') as g:
	# 	res = Stock_data.objects.values('company_id').annotate(max_date=Max('date'))

cleanlog()
	

	

