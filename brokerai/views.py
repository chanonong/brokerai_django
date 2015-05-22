from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
import os
from brokerai.models import *
from brokerai.serializers import *
import json
from datetime import datetime
from rest_framework import generics, permissions
from django.db.models import Max,F
from django.contrib.auth.models import AnonymousUser,User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

# Create your views here.
class HttpAPI:
    def __init__(self,url,description,example_url,is_implemented):
        self.url = url
        self.description = description
        self.example_url = example_url
        self.is_implemented = is_implemented

    def __str__(self):
        return "<ul><li>URL ---------------- {0}</li><li>Description -------- {1}</li><li>Is_implemented --- {2}</li><li>Example ------------ <a href='{3}'>{3}</a></li></ul>".format(self.url,self.description,str(self.is_implemented),self.example_url)

api_forLearnDay = HttpAPI('/api/forlearn/day','learning data for daily for ML in .arff format','/api/forlearn/day',True)
api_forLearnWeek = HttpAPI('/api/forlearn/week','learning data for daily for ML in .arff format','/api/forlearn/week',False)
api_forLearnMonth = HttpAPI('/api/forlearn/month','learning data for daily for ML in .arff format','/api/forlearn/month',False)
api_latest = HttpAPI('/api/forlearn/latest','latest stock for ML in .arff format','/api/forlearn/latest',True)
api_companies = HttpAPI('/api/companies','all companies','/api/companies/',True)
api_companies_id = HttpAPI('/api/companies/:company_id','company by id','/api/companies/1',True)
api_stocks = HttpAPI('/api/stocks/','all stocks','/api/stocks/',True)
api_stocks_id = HttpAPI('/api/stocks/:company_id','all stocks by company id','/api/stocks/3',True)
api_stocks_symbol = HttpAPI('/api/stocks/:symbol','all stocks by company_symbol','/api/stocks/AAPL',True)

api_arr = [api_forLearnDay,api_forLearnWeek,api_forLearnMonth,api_latest,api_companies,api_companies_id,api_stocks,api_stocks_id,api_stocks_symbol]


def index(request):
    messages = ["PLEASE USE FOLLOWING API"]
    for api in api_arr:
        messages += [str(api)]
    return HttpResponse('<hr>'.join(messages))

@api_view(['GET'])
def initCompanies(request):
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'tmp/available_company.txt')
    with open(file_path,'r') as f:
        data = f.readlines()
        print(''.join(data))
    if len(Companies.objects.all()) != 0:
        Companies.objects.all().delete()
    for _ in data:
        c = Companies(name=_.split('\t')[1].strip(), symbol=_.split('\t')[0])
        c.save()
    print(len(Companies.objects.all()))
    return HttpResponse('<br>'.join(data))

# for learning data
def for_learn_day(request):
    companies = Companies.objects.all()#[:100]
    start = request.GET.get('start') or "2014-01-01"
    finish = request.GET.get('finish') or "2014-03-01"
    no_of_set = request.GET.get('count') or 7
    if no_of_set < 7:
        no_of_set = 7
    date_range = [start,finish]
    header = ["@relation test1",""]
    for i in range(no_of_set):
        header += ["@attribute high"+ str(i+1) +" numeric"]
        header += ["@attribute low"+ str(i+1) +" numeric"]
        header += ["@attribute open"+ str(i+1) +" numeric"]
        header += ["@attribute volume"+ str(i+1) +" numeric"]
    header += ["@attribute output numeric","","@data"]

    content = []
    stl = []
    for c in companies:
        s = Stock_data.objects.filter(company_id=c.id,date__range = date_range).order_by('date')[:no_of_set]
        o = Stock_data.objects.filter(company_id=c.id,date__range = date_range).order_by('date')[no_of_set:no_of_set+1]
        stl += [[s,o]]
    for _ in stl:
        if len(_[0]) != 0 and len(_[1]) != 0:
            row = [[str(d.high_price),str(d.low_price),str(d.close_price),str(d.volume)] for d in _[0]]
            flat_row = [item for sublist in row for item in sublist]
            real_output = str(_[1][0].close_price)
            flat_row += [real_output]
            flat_row += [_[0][0].company_id.symbol]
            content += [','.join(flat_row)]
    output = '\n'.join(header + content)
    html_output = '<br>'.join(header + content)
    response = HttpResponse(output)
    return response

def for_learn_week(request):
    companies = Companies.objects.all()#[:100]
    start = request.GET.get('start') or "2014-01-01"
    finish = request.GET.get('finish') or "2014-05-01"
    no_of_set = request.GET.get('count') or 7
    if no_of_set < 7:
        no_of_set = 7
    date_range = [start,finish]
    header = ["@relation test1",""]
    for i in range(no_of_set):
        header += ["@attribute high"+ str(i+1) +" numeric"]
        header += ["@attribute low"+ str(i+1) +" numeric"]
        header += ["@attribute open"+ str(i+1) +" numeric"]
        header += ["@attribute volume"+ str(i+1) +" numeric"]
    header += ["@attribute output numeric","","@data"]

    content = []
    stl = []
    for c in companies:
        s = Stock_data.objects.raw('''SELECT max(id) as id, COALESCE(open_price) as open_price, MIN(low_price ) as low_price, MAX(high_price) as high_price, substring_index(group_concat(close_price order by date desc), ',', 1) as close_price, SUM(volume) as volume, currency, company_id_id, date FROM brokerai_stock_data WHERE company_id_id = ''' + str(c.id) +  ''' and  date BETWEEN "'''+ date_range[0] +'''" and "'''+ date_range[1] +'''" GROUP BY company_id_id,WEEK(date)''')[:no_of_set]
        o = Stock_data.objects.raw('''SELECT max(id) as id, COALESCE(open_price) as open_price, MIN(low_price ) as low_price, MAX(high_price) as high_price, substring_index(group_concat(close_price order by date desc), ',', 1) as close_price, SUM(volume) as volume, currency, company_id_id, date FROM brokerai_stock_data WHERE company_id_id = ''' + str(c.id) +  ''' and  date BETWEEN "'''+ date_range[0] +'''" and "'''+ date_range[1] +'''" GROUP BY company_id_id,WEEK(date)''')[no_of_set:no_of_set+1]
        stl += [[s,o]]
    for _ in stl:
        if len(_[0]) != 0 and len(_[1]) != 0:
            row = [[str(d.high_price),str(d.low_price),str(d.close_price),str(d.volume)] for d in _[0]]
            flat_row = [item for sublist in row for item in sublist]
            real_output = str(_[1][0].close_price)
            flat_row += [real_output]
            flat_row += [_[0][0].company_id.symbol]
            content += [','.join(flat_row)]
    output = '\n'.join(header + content)
    html_output = '<br>'.join(header + content)
    response = HttpResponse(output)
    return response

def for_learn_month(request):
    companies = Companies.objects.all()#[:100]
    start = request.GET.get('start') or "2014-01-01"
    finish = request.GET.get('finish') or "2014-12-01"
    no_of_set = request.GET.get('count') or 7
    if no_of_set < 7:
        no_of_set = 7
    date_range = [start,finish]
    header = ["@relation test1",""]
    for i in range(no_of_set):
        header += ["@attribute high"+ str(i+1) +" numeric"]
        header += ["@attribute low"+ str(i+1) +" numeric"]
        header += ["@attribute open"+ str(i+1) +" numeric"]
        header += ["@attribute volume"+ str(i+1) +" numeric"]
    header += ["@attribute output numeric","","@data"]

    content = []
    stl = []
    for c in companies:
        s = Stock_data.objects.raw('''SELECT max(id) as id, COALESCE(open_price) as open_price, MIN(low_price ) as low_price, MAX(high_price) as high_price, substring_index(group_concat(close_price order by date desc), ',', 1) as close_price, SUM(volume) as volume, currency, company_id_id, date FROM brokerai_stock_data WHERE company_id_id = ''' + str(c.id) +  ''' and  date BETWEEN "'''+ date_range[0] +'''" and "'''+ date_range[1] +'''" GROUP BY company_id_id,DATE_FORMAT(date,'%%Y%%m')''')[:no_of_set]
        o = Stock_data.objects.raw('''SELECT max(id) as id, COALESCE(open_price) as open_price, MIN(low_price ) as low_price, MAX(high_price) as high_price, substring_index(group_concat(close_price order by date desc), ',', 1) as close_price, SUM(volume) as volume, currency, company_id_id, date FROM brokerai_stock_data WHERE company_id_id = ''' + str(c.id) +  ''' and  date BETWEEN "'''+ date_range[0] +'''" and "'''+ date_range[1] +'''" GROUP BY company_id_id,DATE_FORMAT(date,'%%Y%%m')''')[no_of_set:no_of_set+1]
        stl += [[s,o]]
    for _ in stl:
        if len(_[0]) != 0 and len(_[1]) != 0:
            row = [[str(d.high_price),str(d.low_price),str(d.close_price),str(d.volume)] for d in _[0]]
            flat_row = [item for sublist in row for item in sublist]
            real_output = str(_[1][0].close_price)
            flat_row += [real_output]
            flat_row += [_[0][0].company_id.symbol]
            content += [','.join(flat_row)]
    output = '\n'.join(header + content)
    html_output = '<br>'.join(header + content)
    response = HttpResponse(output)
    return response



def latest_day(request):
    companies = Companies.objects.all()
    no_of_set = request.GET.get('set_count') or 7
    no_of_set = int(no_of_set)
    header = ["@relation latest",""]
    for i in range(no_of_set):
        header += ["@attribute high"+ str(i+1) +" numeric"]
        header += ["@attribute low"+ str(i+1) +" numeric"]
        header += ["@attribute open"+ str(i+1) +" numeric"]
        header += ["@attribute volume"+ str(i+1) +" numeric"]
    header += ["@attribute output numeric","","@data"]

    content = []
    stl = []
    for c in companies:
        s = Stock_data.objects.filter(company_id=c.id).order_by('date')[::-1][:no_of_set][::-1]
        stl += [s]
    for _ in stl:
        if len(_) != 0:
            row = [[str(d.high_price),str(d.low_price),str(d.close_price),str(d.volume)] for d in _]
            row = ['?','?','?','?'] * (no_of_set - len(row)) + row
            flat_row = [item for sublist in row for item in sublist]
            flat_row += ['?',_[0].company_id.symbol]
            content += [','.join(flat_row)]
    output = '\n'.join(header + content)
    html_output = '<br>'.join(header + content)
    response = HttpResponse(output)
    return response

def latest_week(request):
    companies = Companies.objects.all()
    no_of_set = request.GET.get('set_count') or 7
    no_of_set = int(no_of_set)
    header = ["@relation latest",""]
    for i in range(no_of_set):
        header += ["@attribute high"+ str(i+1) +" numeric"]
        header += ["@attribute low"+ str(i+1) +" numeric"]
        header += ["@attribute open"+ str(i+1) +" numeric"]
        header += ["@attribute volume"+ str(i+1) +" numeric"]
    header += ["@attribute output numeric","","@data"]

    content = []
    stl = []
    for c in companies:
        s = Stock_data.objects.raw('''SELECT max(id) as id, COALESCE(open_price), MIN(low_price ), MAX(high_price), substring_index(group_concat(close_price order by date desc), ',', 1) as close_price, SUM(volume), currency, company_id_id, date FROM brokerai_stock_data WHERE company_id_id=''' + str(c.id) + ''' GROUP BY company_id_id,WEEK(date)''')[::-1][:no_of_set][::-1]
        stl += [s]
    for _ in stl:
        if len(_) != 0:
            row = [[str(d.high_price),str(d.low_price),str(d.close_price),str(d.volume)] for d in _]
            row = ['?','?','?','?'] * (no_of_set - len(row)) + row
            flat_row = [item for sublist in row for item in sublist]
            flat_row += ['?',_[0].company_id.symbol]
            content += [','.join(flat_row)]
    output = '\n'.join(header + content)
    html_output = '<br>'.join(header + content)
    response = HttpResponse(output)
    return response

def latest_month(request):
    companies = Companies.objects.all()
    no_of_set = request.GET.get('set_count') or 7
    no_of_set = int(no_of_set)
    header = ["@relation latest",""]
    for i in range(no_of_set):
        header += ["@attribute high"+ str(i+1) +" numeric"]
        header += ["@attribute low"+ str(i+1) +" numeric"]
        header += ["@attribute open"+ str(i+1) +" numeric"]
        header += ["@attribute volume"+ str(i+1) +" numeric"]
    header += ["@attribute output numeric","","@data"]

    content = []
    stl = []
    for c in companies:
        s = Stock_data.objects.raw('''SELECT max(id) as id, COALESCE(open_price), MIN(low_price), MAX(high_price), substring_index(group_concat(close_price order by date desc), ',', 1) as close_price, SUM(volume), currency, company_id_id, date FROM brokerai_stock_data WHERE company_id_id=''' + str(c.id) + ''' GROUP BY company_id_id,DATE_FORMAT(date,'%%Y%%m')''')[::-1][:no_of_set][::-1]
        stl += [s]
    for _ in stl:
        if len(_) != 0:
            row = [[str(d.high_price),str(d.low_price),str(d.close_price),str(d.volume)] for d in _]
            row = ['?','?','?','?'] * (no_of_set - len(row)) + row
            flat_row = [item for sublist in row for item in sublist]
            flat_row += ['?',_[0].company_id.symbol]
            content += [','.join(flat_row)]
    output = '\n'.join(header + content)
    html_output = '<br>'.join(header + content)
    response = HttpResponse(output)
    return response



@csrf_exempt
@api_view(['GET'])
def companies_list(request):
    if request.method == 'GET':
        companies = Companies.objects.all()
        serializer = CompaniesSerializer(companies, many=True)
        return JSONResponse(serializer.data)

@csrf_exempt
@api_view(['GET'])
def companies_list_id(request,cid=None):
    if request.method == 'GET':
        companies = Companies.objects.filter(id=cid)[0]
        serializer = CompaniesSerializer(companies, many=False)
        return JSONResponse(serializer.data)
@csrf_exempt
def stock_data_company_id(request,cid=None):
    if request.method == 'GET':
        stock = Stock_data.objects.filter(company_id_id=cid)
        serializer = StockDataSerializer(stock, many=True)
        return JSONResponse(serializer.data)
@csrf_exempt
def stock_data_company_symbol(request,symbol=None):
    if request.method == 'GET':
        company = Companies.objects.filter(symbol=symbol)
        stock = Stock_data.objects.filter(company_id=company)
        serializer = StockDataSerializer(stock, many=True)
        return JSONResponse(serializer.data)

@csrf_exempt
@api_view(['GET','POST'])
def stock_data(request):
    """
    List all companies, or create a new companies
    """
    if request.method == 'GET':
        stock = Stock_data.objects.all().order_by('-date')[:5000][::-1]
        serializer = StockDataSerializer(stock, many=True)
        return JSONResponse(serializer.data)

@api_view(['GET'])
def latest_stock(request):
    if request.method == 'GET':
        get_type = request.GET.get('type') or "day"
        if get_type == "day":
            stock_day = Stock_data.objects.raw('''SELECT max(id) as id,substring_index(group_concat(open_price order by date desc), ',', 1) as open_price, substring_index(group_concat(low_price order by date desc), ',', 1) as low_price, substring_index(group_concat(high_price order by date desc), ',', 1) as high_price, substring_index(group_concat(close_price order by date desc), ',', 1) as close_price, substring_index(group_concat(volume order by date desc), ',', 1) as volume, currency, company_id_id, max(date) as date FROM brokerai_stock_data GROUP BY company_id_id''')
            stock = stock_day
        elif get_type == "week":
            stock_week = Stock_data.objects.raw('''SELECT max(id) as id, COALESCE(open_price), MIN(low_price ), MAX(high_price), substring_index(group_concat(close_price order by date desc), ',', 1) as close_price, SUM(volume), currency, company_id_id, date FROM brokerai_stock_data WHERE date BETWEEN SUBDATE(CURDATE(), INTERVAL 1 WEEK) AND NOW() GROUP BY company_id_id''')
            stock = stock_week
        elif get_type == "month":
            stock_month = Stock_data.objects.raw('''SELECT max(id) as id, COALESCE(open_price), MIN(low_price ), MAX(high_price), substring_index(group_concat(close_price order by date desc), ',', 1) as close_price, SUM(volume), currency, company_id_id, date FROM brokerai_stock_data WHERE date BETWEEN SUBDATE(CURDATE(), INTERVAL 1 MONTH) AND NOW() GROUP BY company_id_id''')
            stock = stock_month
        else:
            return HttpResponse("wrong type bro!",status=409)
        paginator = Paginator(list(stock), 25)        

        page = request.GET.get('page')
        if page:
            try:
                stock = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                stock = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                stock = paginator.page(paginator.num_pages)
        serializer = StockDataSerializer(stock, many=True)
        return JSONResponse(serializer.data)
@api_view(['GET'])
def latest_stock_company_id(request,cid=None):
    if request.method == 'GET':
        get_type = request.GET.get('type') or "day"
        if get_type == "day":
            stock_day = Stock_data.objects.raw('''SELECT max(id) as id,substring_index(group_concat(open_price order by date desc), ',', 1) as open_price, substring_index(group_concat(low_price order by date desc), ',', 1) as low_price, substring_index(group_concat(high_price order by date desc), ',', 1) as high_price, substring_index(group_concat(close_price order by date desc), ',', 1) as close_price, substring_index(group_concat(volume order by date desc), ',', 1) as volume, currency, company_id_id, max(date) as date FROM brokerai_stock_data WHERE company_id_id = ''' + cid)
            stock = stock_day
        elif get_type == "week":
            stock_week = Stock_data.objects.raw('''SELECT max(id) as id, COALESCE(open_price), MIN(low_price ), MAX(high_price), substring_index(group_concat(close_price order by date desc), ',', 1) as close_price, SUM(volume), currency, company_id_id, date FROM brokerai_stock_data WHERE date BETWEEN SUBDATE(CURDATE(), INTERVAL 1 WEEK) AND NOW() WHERE company_id_id = ''' + cid)
            stock = stock_week
        elif get_type == "month":
            stock_month = Stock_data.objects.raw('''SELECT max(id) as id, COALESCE(open_price), MIN(low_price ), MAX(high_price), substring_index(group_concat(close_price order by date desc), ',', 1) as close_price, SUM(volume), currency, company_id_id, date FROM brokerai_stock_data WHERE date BETWEEN SUBDATE(CURDATE(), INTERVAL 1 MONTH) AND NOW() WHERE company_id_id = ''' + cid)
            stock = stock_month
        else:
            return HttpResponse("wrong type bro!",status=409)
        
        paginator = Paginator(list(stock), 25)
        page = request.GET.get('page')
        if page:
            try:
                stock = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                stock = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                stock = paginator.page(paginator.num_pages)
        serializer = StockDataSerializer(stock, many=True)
        return JSONResponse(serializer.data)

@csrf_exempt
@api_view(['GET','POST'])
def predicted_data(request):
    """
    List all companies, or create a new companies
    """
    if request.method == 'GET':
        #predicted = Predicted_data.objects.all()
        company = Companies.objects.all()
        predicted = Predicted_data.objects.raw('''SELECT Max(id) as id, stock_id_id, nn_daily, nn_weekly, nn_monthly, dt_daily, dt_weekly, dt_monthly, bs_daily_buy, bs_daily_sell, bs_daily_recommend, bs_weekly_buy,bs_weekly_sell,bs_weekly_recommend, bs_monthly_buy,bs_monthly_sell,bs_monthly_recommend FROM brokerai_predicted_data GROUP BY stock_id_id ORDER BY id DESC LIMIT 0,''' + str(len(company)))
        serializer = PredictedDataSerializer(predicted, many=True)
        return JSONResponse(serializer.data)

@csrf_exempt
@api_view(['GET','POST'])
def predicted_data_company_id(request,cid=None):
    """
    List all companies, or create a new companies
    """
    if request.method == 'GET':
        s = Stock_data.objects.filter(company_id_id=cid)[::-1][0]
        print(s)
        #predicted = Predicted_data.objects.all()
        predicted = Predicted_data.objects.raw('''SELECT id, stock_id_id, nn_daily, nn_weekly, nn_monthly, dt_daily, dt_weekly, dt_monthly, bs_daily_buy, bs_daily_sell, bs_daily_recommend, bs_weekly_buy,bs_weekly_sell,bs_weekly_recommend, bs_monthly_buy,bs_monthly_sell,bs_monthly_recommend FROM brokerai_predicted_data WHERE stock_id_id =''' + str(s.id))
        serializer = PredictedDataSerializer(predicted, many=True)
        return JSONResponse(serializer.data)

@csrf_exempt
@api_view(['POST'])
def register(request):
    VALID_USER_FIELDS = [f.name for f in User._meta.fields]
    DEFAULTS = {
        # you can define any defaults that you would like for the user, here
    }
    serialized = UserSerializer(data=request.DATA)
    if serialized.is_valid():
        user = serialized.save()
        return JSONResponse(UserSerializer(instance=user).data, status=201)#status.HTTP_201_CREATED)
    else:
        print(serialized._errors)
        return JSONResponse(serialized._errors, status=400)

@csrf_exempt
@api_view(['GET','PUT'])
def users(request):
    print(request.user)
    if not isinstance(request.user,AnonymousUser):
        if request.method == 'GET':
            #user = User.objects.all()
            user = request.user
            serializer = UserSerializer(user, many=False)
            return JSONResponse(serializer.data)
        elif request.method == 'PUT':
            serializer = UserSerializer(data=request.DATA)
            if serializer.is_valid():
                serializer.update()
                return JSONResponse(serializer.data, status=201)
            return JSONResponse(serializer.errors, status=400)
    else:
        return HttpResponse(status=404)

@csrf_exempt
@api_view(['GET','POST','DELETE'])
def user_favorite(request):
    """
    List all companies, or create a new companies
    """
    
    if request.method == 'GET':
        if not isinstance(request.user,AnonymousUser):
            favorite = User_favorite.objects.filter(user_id_id=request.user.id)#.all()
            serializer = UserFavoriteSerializer(favorite, many=True)
            return JSONResponse(serializer.data)
        else:
            return HttpResponse('Please Login!',status=401)
    elif request.method == 'POST':
        if not isinstance(request.user,AnonymousUser):
            if str(request.DATA.get('user_id')) == str(request.user.id):
                serializer = UserFavoriteSerializer(data=request.DATA)
                if serializer.is_valid():
                    serializer.save()
                    return JSONResponse(serializer.data, status=201)
                return JSONResponse(serializer.errors, status=400)
            else:
                return HttpResponse("dont try to use different user id to save :) your user_id is " + str(request.user.id),status=409)
        else:
            return HttpResponse('Please Login!',status=401)
    elif request.method == "DELETE":
        if not isinstance(request.user,AnonymousUser):
            if str(request.DATA.get('user_id')) == str(request.user.id):
                favorite = User_favorite.objects.filter(user_id_id=str(request.DATA.get('user_id')),company_id_id=str(request.DATA.get('company_id')))
                if len(favorite) > 0:
                    User_favorite.delete(favorite[0])
                    message = "DELETE " + request.DATA.get('user_id') + " " + request.DATA.get('company_id')
                    return JSONResponse(message, status=200)
                return JSONResponse('NOT FOUND', status=404)
            else:
                return HttpResponse("dont try to use different user id to save :) your user_id is " + str(request.user.id),status=409)
        else:
            return HttpResponse('Please Login!',status=401)       
