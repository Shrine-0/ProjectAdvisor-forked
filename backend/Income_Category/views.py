from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import IncomeCategory
from .serializers import CategoryIncomeSerializer
# Create your views here.

class CategoryListView(APIView):
    
    # == Authentication ==
    
    permission_classes = [IsAuthenticated]
    
    # for retriving the category
    def get(self, request, format = None):
        try:
            incCategory = IncomeCategory.objects.filter(user=request.user)
            serializer = CategoryIncomeSerializer(incCategory, many=True)
            data = {"filtered": serializer.data}
            return Response(data, status=status.HTTP_200_OK)

        except:
            return Response(
                data={"message": "Unable to get categories"}, status=status.HTTP_400_BAD_REQUEST
            )
    
    # === FOr posting the category ===
    def post(self, request):
        try:
            data = request.data
            incCategory = IncomeCategory.objects.create(name=data["name"], user=request.user)
            serializer = CategoryIncomeSerializer(incCategory, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(
                data={"message": "Unable to create category"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

class CategoryDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return IncomeCategory.objects.get(pk=pk)
        except IncomeCategory.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        incCategory = self.get_object(pk)
        if request.user == incCategory.user:
            try:
                serializer = CategoryIncomeSerializer(incCategory)
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

    def put(self, request, pk):
        incCategory = self.get_object(pk)
        if request.user == incCategory.user:
            try:
                serializer = CategoryIncomeSerializer(incCategory, data=request.data)
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

    def delete(self, request, pk):
        incCategory = self.get_object(pk)
        if request.user == incCategory.user:
            incCategory.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                data={"message": "Forbidden, Not Authorized"},
                status=status.HTTP_403_FORBIDDEN,
            )