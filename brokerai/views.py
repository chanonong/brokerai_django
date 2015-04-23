from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import api_view
import os
from brokerai.models import *
from brokerai.serializers import *
import json
from datetime import datetime
from rest_framework import generics, permissions

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@api_view(['GET'])
def initCompanies(request):
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'tmp/available_company.txt')
    with open(file_path,'r') as f:
        data = f.readlines()
        print(''.join(data))
    # print lenght of existing company
    if len(Companies.objects.all()) != 0:
        Companies.objects.all().delete()
    for _ in data:
        c = Companies(name=_.split('\t')[1].strip(), symbol=_.split('\t')[0])
        c.save()
    print(len(Companies.objects.all()))
    return HttpResponse('<br>'.join(data))

# for learning data
def forLearn(request):
    companies = Companies.objects.all()#[:100]
    #date_range = ["2014-06-01","2014-07-01"]
    start = request.GET.get('start') or "2014-06-01"
    finish = request.GET.get('finish') or "2014-07-01"
    # if start is None:
    #     start = "2014-06-01"
    # if finish is None:
    #     finish = "2014-07-01"
    date_range = [start,finish]
    no_of_set = 7
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
        #     print(content)
        #print(','.join([str(d.open_price) for d in _]))
    #print(companiesList)
    # for s in stock:
    #     print(list(map(str,[s.high_price,s.low_price,s.close_price,s.volume])))
    output = '\n'.join(header + content)
    html_output = '<br>'.join(header + content)
    response = HttpResponse(output, content_type='application/text')
    response['Content-Disposition'] = 'attachment; filename="test.arff"'
    return response

def latest(request):
    companies = Companies.objects.all()#[:100]
    #date_range = ["2014-06-01","2014-07-01"]
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
        s = Stock_data.objects.filter(company_id=c.id).order_by('date')[::-1][:no_of_set]
        stl += [s]
    for _ in stl:
        if len(_) != 0:
            row = [[str(d.high_price),str(d.low_price),str(d.close_price),str(d.volume)] for d in _]
            flat_row = [item for sublist in row for item in sublist]
            flat_row += [_[0].company_id.symbol]
            content += [','.join(flat_row)]
        #     print(content)
        #print(','.join([str(d.open_price) for d in _]))
    #print(companiesList)
    # for s in stock:
    #     print(list(map(str,[s.high_price,s.low_price,s.close_price,s.volume])))
    output = '\n'.join(header + content)
    html_output = '<br>'.join(header + content)
    response = HttpResponse(output, content_type='application/text')
    response['Content-Disposition'] = 'attachment; filename="latest.arff"'
    return response

# Create your views here.
def index(request):
    all_companies = Companies.objects.all();
    output = ','.join(all_companies)
    print(output)
    return HttpResponse('[' + output +']')

@csrf_exempt
@api_view(['GET','POST'])
def companies_list(request):
    """
    List all companies, or create a new companies
    """
    if request.method == 'GET':
        companies = Companies.objects.all()
        serializer = CompaniesSerializer(companies, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CompaniesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


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

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = StockDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(['GET','POST'])
def predicted_data(request):
    """
    List all companies, or create a new companies
    """
    if request.method == 'GET':
        predicted = Predicted_data.objects.all()
        serializer = PredictedDataSerializer(predicted, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PredictedDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(['POST'])
def register(request):
    VALID_USER_FIELDS = [f.name for f in User._meta.fields]
    DEFAULTS = {
        # you can define any defaults that you would like for the user, here
    }
    serialized = UserSerializer(data=request.DATA)
    if serialized.is_valid():
        user_data = {field: data for (field, data) in request.DATA.items() if field in VALID_USER_FIELDS}
        user_data.update(DEFAULTS)
        user = User.objects.create_user(
            **user_data
        )
        return HttpResponse(UserSerializer(instance=user).data, status=201)#status.HTTP_201_CREATED)
    else:
        return HttpResponse(serialized._errors, status=400)#status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET','POST'])
def users(request):
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

# class UserListCreateAPIView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def get_permissions(self):
#         if self.request.method in permissions.SAFE_METHODS:
#             return (permissions.IsAuthenticated(),)
#         return (permissions.AllowAny(),)

@csrf_exempt
@api_view(['GET','POST'])
def user_favorite(request):
    """
    List all companies, or create a new companies
    """
    if request.method == 'GET':
        favorite = UserFavorite.objects.all()
        serializer = UserFavoriteSerializer(favorite, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserFavoriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)