from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


# ==Import from Locals==
from Expenses.models import Expenses
from Expenses.serializers import ExpenseSerializer


# === Creating and getting all Expenses view ===
class ExpensesListView(APIView):
    
    #=== Adding permission ===
    permission_classes = [IsAuthenticated]
    
    # === Getting all the Expenses list ===
    def get(self, request):
        try:
            results = (
                Expenses.objects.filter(user=request.user)
                # .filter(date__month=str(current_month))
                .order_by("id")
            )
            serializer = ExpenseSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to retrieve expenses"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    # === Adding new data ===
    # def post(self, request):
    #     try:
    #         data = request.data
    #         expense = Expenses.objects.create(
    #             name=data["name"],
    #             amount=data["amount"],
    #             description=data["note"],
    #             exCategory_id=data["exCategory"],
    #             user=request.user,
    #         )
    #         serializer = ExpenseSerializer(expense, many=False)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except:
    #         return Response(
    #             data={"message": "Unable to create expense"},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# === Class that handles specific Expenses ===
class ExpensesDetailView(APIView):
    
    #=== Adding permission ===
    permission_classes = [IsAuthenticated]

    #===Getting Specific Details
    def get_object(self, pk):
        try:
            return Expenses.objects.get(pk=pk)
        except Expenses.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        expense = self.get_object(pk)
        if request.user == expense.user:
            serializer = ExpenseSerializer(expense)
            return Response(serializer.data)
        else:
            return Response(
                data={"message": "Forbidden, Not Authorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    
    # === Editing the Expenses ===
    # def put(self, request, pk):
    #     expense = self.get_object(pk)
    #     data = request.data
    #     if request.user == expense.user:
    #         expense.name = data["name"]
    #         expense.amount = data["amount"]
    #         expense.description = data["note"]
    #         expense.exCategory_id = data["exCategory"]

    #         serializer = ExpenseSerializer(expense, data=request.data, partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response(
    #             data={"message": "Forbidden, Not Authorized"},
    #             status=status.HTTP_401_UNAUTHORIZED,
    #         )
    
    
    def put(self, request, pk):
        expense = self.get_object(pk)
        if expense.user == request.user:
            serializer = ExpenseSerializer(expense, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": "Forbidden, Not Authorized"},
            status=status.HTTP_403_FORBIDDEN,
        )
    
    # === Deleting the Expenses ===
    def delete(self, request, pk):
        expense = self.get_object(pk)
        if request.user == expense.user:
            expense.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                data={"message": "Forbidden, Not Authorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )