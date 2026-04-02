from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import JobPosting
from .serializers import JobPostingSerializer


class JobPostingFilter(filters.FilterSet):
    location = filters.CharFilter(field_name='location', lookup_expr='icontains')

    class Meta:
        model = JobPosting
        fields = ['location']


class JobPostingListView(generics.ListAPIView):
    """
    Lists all job postings related on field of Technology, newest first.
    Premium-only fields are masked for unauthenticated or Basic users.

    """
    queryset = JobPosting.objects.all().order_by('-created_at')
    serializer_class = JobPostingSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = JobPostingFilter              
    search_fields = ['title', 'description']       
    ordering_fields = ['created_at']
    ordering = ['-created_at']                     


class JobPostingDetailView(generics.RetrieveAPIView):
    """
    GET /api/jobs/<id>/

    Returns a single job posting.
    Same field-level masking applies based on the requester's membership tier.
    """
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [AllowAny]
