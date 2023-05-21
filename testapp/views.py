from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, mixins
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, \
    get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, GenericViewSet, ModelViewSet
from .models import Employee
from .serializers import EmployeeSerializer, EmployeeModelSerializer



# ****************************************************************************
# Function based views
# ****************************************************************************
# Normal FBV
# ----------------------------------------------------------------------------
@csrf_exempt
def employeeview(request):
    if request.method == 'GET':
        qs = Employee.objects.all()
        serializer = EmployeeSerializer(qs, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        pdata = JSONParser().parse(request)
        serializer = EmployeeSerializer(data=pdata)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
@csrf_exempt
def employeedetailview(request, id):
    try:
        emp = Employee.objects.get(id=id)
    except Employee.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = EmployeeSerializer(emp)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        pdata = JSONParser().parse(request)
        serializer = EmployeeSerializer(emp, data=pdata)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        emp.delete()
        return HttpResponse(status=200)
# ----------------------------------------------------------------------------
# decorator FBV
# ----------------------------------------------------------------------------
@api_view(['GET', 'POST'])
def employeedecoAPIView(request):
    if request.method == 'GET':
        qs = Employee.objects.all()
        serializer = EmployeeModelSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'PUT', 'DELETE'])
def employeedetaildecoAPIView(request, id):
    try:
        emp = Employee.objects.get(id=id)
    except Employee.DoesNotExist:
        msg = {'msg': 'Resource does not exist for given data'}
        return JsonResponse(msg, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = EmployeeSerializer(emp)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = EmployeeSerializer(emp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        emp.delete()
        return Response(status=status.HTTP_200_OK)
# **************************************************************
# Class Based Views (CBV)
# **************************************************************
# APIViews
# --------------------------------------------------------------
class EmployeeAPIView(APIView):
    def get(self, request):
        qs = Employee.objects.all()
        serializer = EmployeeSerializer(qs, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class EmployeeDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def get(self, request, id):
        employee = self.get_object(id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    def put(self, request, id):
        employee = self.get_object(id)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id):
        employee = self.get_object(id)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# --------------------------------------------------------------
# Generic_APIViews_CBV
# --------------------------------------------------------------
class EmployeeListCreateAPIView(ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
class EmployeeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'id'
# --------------------------------------------------------------
# Generic_APIViews_CBV_mixins
# --------------------------------------------------------------
class EmployeeListCreateModelMixin(mixins.CreateModelMixin, ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
class EmployeeRetrieveUpdateDistroyModelMixin(mixins.UpdateModelMixin, mixins.DestroyModelMixin, RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
# --------------------------------------------------------------
# ViewSet
# --------------------------------------------------------------
class EmployeeViewset(ViewSet):
    def list(self, request):
        emps = Employee.objects.all()
        serializer = EmployeeSerializer(emps, many=True)
        return Response(serializer.data)
    def create(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        queryset = Employee.objects.all()
        emp = get_object_or_404(queryset, pk=pk)
        serializer = EmployeeSerializer(emp)
        return Response(serializer.data)
    def update(self, request, pk=None):
        emp = Employee.objects.get(pk=pk)
        serializer = EmployeeSerializer(emp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, pk=None):
        emp = Employee.objects.get(pk=pk)
        emp.delete()
        msg = {'msg': 'Resource deleted successfully'}
        return Response(msg, status=status.HTTP_200_OK)
# --------------------------------------------------------------
# ViewSet_modelmixins
# --------------------------------------------------------------
class EmployeeGenericViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                             mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'id'
    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)
    def post(self, request):
        return self.create(request)
    def put(self, request, id=None):
        return self.update(request, id)
    def patch(self, request, id=None):
        return self.partial_update(request, id)
    def delete(self, request, id):
        return self.destroy(request, id)
# --------------------------------------------------------------
# ModelMixins
# --------------------------------------------------------------
class EmployeeCBViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
# --------------------------------------------------------------
