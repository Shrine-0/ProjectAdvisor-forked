# from django.shortcuts import render
# from django.http import Http404
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView


# # ==Import from Locals==
# from Expenses.models import Expenses
# from Expenses.serializers import ExpenseSerializer

# # === Adding search filter
# from rest_framework.filters import SearchFilter

# === Creating and getting all Expenses view ===
# class ExpensesListView(APIView):
    
#     #=== Adding permission ===
#     permission_classes = [IsAuthenticated]
    
#     # === Getting all the Expenses list ===
#     def get(self, request):
#         try:
#             results = (
#                 Expenses.objects.filter(user=request.user)
#                 # .filter(date__month=str(current_month))
#                 .order_by("id")
#             )
#             serializer = ExpenseSerializer(results, many=True)
#             filter_backends = [SearchFilter]
#             search_fields = [ 'name']
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except:
#             return Response(
#                 data={"message": "Unable to retrieve expenses"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
    
#     # === Adding new data ===
    
#     def post(self, request):
#         serializer = ExpenseSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # === Class that handles specific Expenses ===
# class ExpensesDetailView(APIView):
    
#     #=== Adding permission ===
#     permission_classes = [IsAuthenticated]

#     #===Getting Specific Details / Dealing with ids.
#     def get_object(self, pk):
#         try:
#             return Expenses.objects.get(pk=pk)
#         except Expenses.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         expense = self.get_object(pk)
#         if request.user == expense.user:
#             serializer = ExpenseSerializer(expense)
#             return Response(serializer.data)
#         else:
#             return Response(
#                 data={"message": "Forbidden, Not Authorized"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )
    
#     # === Editing the Expenses ===
    
    
#     def put(self, request, pk):
#         expense = self.get_object(pk)
#         if expense.user == request.user:
#             serializer = ExpenseSerializer(expense, data=request.data, partial = True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response(
#             {"message": "Forbidden, Not Authorized"},
#             status=status.HTTP_403_FORBIDDEN,
#         )
    
#     # === Deleting the Expenses ===
#     def delete(self, request, pk):
#         expense = self.get_object(pk)
#         if request.user == expense.user:
#             expense.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response(
#                 data={"message": "Forbidden, Not Authorized"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )






# === Using Generic API
from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView

# ==Import from Locals==
from Expenses.models import Expenses
from Expenses.serializers import ExpenseSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from .PaginationFiles.cursorPagination import myPagination

# === Creating and getting all Expenses usuing generic API ===
class ExpensesListView(ListAPIView, CreateAPIView):
    
    # ==== Adding Permission ====
    permission_classes = [IsAuthenticated]
    queryset = Expenses.objects.all()
    serializer_class = ExpenseSerializer
    
    # === Adding Search Filter ===
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name','note', 'amount', 'created_date']
    
    # === Adding Pagination ===
    pagination_class = myPagination
    
    
    # # === Fetching data created by the user
    def get_queryset(self):
        return Expenses.objects.filter(user=self.request.user).order_by('-created_date')

         # .filter(date__month=str(current_month))
#                 .order_by("id")
    
    
    
    # === Creating/ Posting data
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        



# === Class that handles specific Expenses ===
class ExpensesDetailView(RetrieveUpdateAPIView, DestroyAPIView):
    #=== Adding permission ===
    permission_classes = [IsAuthenticated]
    queryset = Expenses.objects.all()
    serializer_class = ExpenseSerializer

    def get_object(self):
        pk = self.kwargs["pk"]
        try:
            return Expenses.objects.get(pk=pk, user=self.request.user)
        except Expenses.DoesNotExist:
            raise Http404