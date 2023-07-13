# === Using Generic API
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView

# ==Import from Locals==
from Todo.models import TodoList
from Todo.serializers import TodoListSerializer
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
    # pagination_class = myPagination
    
    
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