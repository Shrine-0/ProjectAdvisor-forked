from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Income.models import Income

from Income.serializers import IncomeSerializer
# Create your views here.


class IncomeListView(APIView):
    permission_classes = [IsAuthenticated]
    
    # Retrieving all the Incomes
    def get(self, request, format=None):
        try:
            results = (
                Income.objects.all()
                .filter(user=request.user)
                # .filter(date_month = str(current_month))
            )
            serializer = IncomeSerializer(results, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to retrieve income"}, status=status.HTTP_401_UNAUTHORIZED
            )
            
        
    # # Inserting the Income
    def post(self, request, format=None):
        try:
            data = request.data
            income = Income.objects.create(
                incCategory = data["incCategory"],
                amount = data['amount'],
                ntoe = data['note'],
                user = request.user,
                                
            )
            
            serializer = IncomeSerializer(income, many =False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except:
            return Response(
                data={"message": "Unable to Add New Income"}, status=status.HTTP_400_BAD_REQUEST
            )


    
# === IncomeDetailView ===
class IncomeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Income.objects.get(pk=pk)
        except Income.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        income = self.get_object(pk)
        if request.user == income.user:
            serializer = IncomeSerializer(income)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            raise Response(data={"message": "Not permitted"}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        income = self.get_object(pk)
        if request.user == income.user:
            serializer = IncomeSerializer(income, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise Http404

    def delete(self, request, pk):
        income = self.get_object(pk)
        if request.user == income.user:
            income.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise Http404