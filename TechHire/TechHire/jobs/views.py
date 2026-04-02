from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import JobPosting
from .serializers import JobPostingSerializer


class JobPostingListView(generics.ListAPIView):
    """
    GET /api/jobs/

   
    queryset = JobPosting.objects.all().order_by('-created_at')
    serializer_class = JobPostingSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['location']          # ?location=Remote
    search_fields = ['title', 'description'] # ?search=python
    ordering_fields = ['created_at']
    ordering = ['-created_at']              # Default: newest first


class JobPostingDetailView(generics.RetrieveAPIView):
    """
    GET /api/jobs/<id>/

    Returns a single job posting.
    Same field-level masking applies based on the requester's membership tier.
    """
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [AllowAny]
