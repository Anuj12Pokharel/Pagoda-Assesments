######serializers.py######
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)  # shows username by default

    class Meta:
        model = Task
        fields = ("id", "title", "description", "status", "created_by", "created_at", "updated_at")
        read_only_fields = ("id", "created_by", "created_at", "updated_at")

    def create(self, validated_data):
        request = self.context.get("request")
    
        if request and hasattr(request, "user"):
            validated_data["created_by"] = request.user
        return super().create(validated_data)




####Permissions.py######

from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Allow safe methods for authenticated users, but allow unsafe methods only to resource owner.
    """
    def has_permission(self, request, view):
        # require authentication for all actions; adjust if you want list to be public
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # safe methods allowed (list/retrieve are allowed by other logic), but object-level write allowed only to owner
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by_id == request.user.id


####views.py######

from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwner

class TaskViewSet(viewsets.ModelViewSet):
    """
    - list: returns tasks belonging to request.user
    - create: creates task and sets created_by=request.user
    - retrieve/update/destroy: allowed only if owner (IsOwner)
    Supports filtering by ?status=COMPLETED (and others).
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]  # IsOwner implements object-level checks

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status"]   # enables ?status=PENDING
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "updated_at"]

    def get_queryset(self):
        qs = Task.objects.filter(created_by=self.request.user)
        return qs.select_related("created_by")
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)



#########urls.py#######
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("", include(router.urls)),
]
