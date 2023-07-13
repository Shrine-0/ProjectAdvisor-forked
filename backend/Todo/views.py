# === Using Generic API
from django.http import Http404
from rest_framework.response import Response
from django.db import models
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import APIException


# ==Import from Locals==
from Todo.models import TodoList
from Todo.serializers import TodoListSerializer, AmountSerializer
from rest_framework.filters import SearchFilter, OrderingFilter

from Todo.PaginationFiles.cursorPagination import myPagination



# === Creating and getting all Expenses usuing generic API ===
class TodoListView(ListAPIView, CreateAPIView):
    
    # ==== Adding Permission ====
    permission_classes = [IsAuthenticated]
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    
    # === Adding Search Filter ===
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title','type', 'date']
    orderring_fields = ['title','type', 'date']
    
    # === Adding Pagination ===
    pagination_class = myPagination
    
    
    # # === Fetching data created by the user
    def get_queryset(self):
        return TodoList.objects.filter(user=self.request.user).order_by('-created_date')

    
    
    # === Creating/ Posting data
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        



# === Class that handles specific Expenses ===
class TodoListDetailView(RetrieveUpdateAPIView, DestroyAPIView):
    #=== Adding permission ===
    permission_classes = [IsAuthenticated]
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer

    def get_object(self):
        pk = self.kwargs["pk"]
        try:
            return TodoList.objects.get(pk=pk, user=self.request.user)
        except TodoList.DoesNotExist:
            raise Http404





### === To fetch Receivable and Payable amount ===
class AmountView(APIView):
    def get(self, request):
        try:
            receivable_amount = TodoList.objects.filter(type=TodoList.RECEIVABLE).aggregate(total_amount=models.Sum('amount'))['total_amount']
            payable_amount = TodoList.objects.filter(type=TodoList.PAYABLE).aggregate(total_amount=models.Sum('amount'))['total_amount']
        
            serializer = AmountSerializer({
                'receivable_amount': receivable_amount or 0,
                'payable_amount': payable_amount or 0,
            })
        
            return Response({'data': serializer.data})  # Wrap the data in a dictionary
        except Exception as e:
            raise APIException(str(e))


