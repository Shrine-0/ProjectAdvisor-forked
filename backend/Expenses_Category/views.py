from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# === Importing necessary model and serializers
from .models import ExpensesCategory
from .serializers import CategoryExpenseSerializer


class ExpensesCategoryListView(APIView):
    
    # === Adding the permission
    permission_classes = [IsAuthenticated]

    
    # === Getting all category related to user ===
    def get(self, request, format=None):
        try:
            exCategory = ExpensesCategory.objects.filter(user=request.user)
            serializer = CategoryExpenseSerializer(exCategory, many=True)
            data = {"filtered": serializer.data}
            return Response(data, status=status.HTTP_200_OK)

        except:
            return Response(
                data={"message": "Unable to get categories"}, status=status.HTTP_400_BAD_REQUEST
            )
            
    
    # == Inserting new Category
    def post(self, request):
        try:
            data = request.data
            exCategory = ExpensesCategory.objects.create(name=data["name"], user=request.user)
            serializer = CategoryExpenseSerializer(exCategory, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(
                data={"message": "Unable to create category"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

class ExpensesCategoryDetailView(APIView):
    
    # === Adding the permission
    permission_classes = [IsAuthenticated]
    
    # === Getting specific Category ===
    def get_object(self, pk):
        try:
            return ExpensesCategory.objects.get(pk = pk)
        except ExpensesCategory.DoesNotExist:
            raise Http404
        
    
    # === Getting Specific Category ===
    def get(self, request, pk):
        exCategory = self.get_object(pk)
        if request.user == exCategory.user:
            try:
                serializer = CategoryExpenseSerializer(exCategory)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(
                    data={"message": "Unable to get category detail"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                data={"message": "Forbidden, Not Authorized"},
                status=status.HTTP_403_FORBIDDEN,
            )

    
    # === Updating the Expenses Category ===
    def put(self, request, pk):
        exCategory = self.get_object(pk)
        if request.user == exCategory.user:
            try:
                serializer = CategoryExpenseSerializer(exCategory, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        data={"message": "Invalid parameters"}, status=status.HTTP_400_BAD_REQUEST
                    )
            except:
                return Response(
                    data={"message": "Unable to update category"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                data={"message": "Forbidden, Not Authorized"},
                status=status.HTTP_403_FORBIDDEN,
            )

    # === Deleting the Expenses Category ===
    def delete(self, request, pk):
        exCategory = self.get_object(pk)
        if request.user == exCategory.user:
            exCategory.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                data={"message": "Forbidden, Not Authorized"},
                status=status.HTTP_403_FORBIDDEN,
            )