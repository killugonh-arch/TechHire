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
    GET /api/jobs/

    Lists all job postings, newest first.
    Premium-only fields are masked for unauthenticated / Basic users.

    Query parameters:
      ?search=<term>       – searches title & description (case-insensitive)
      ?location=<value>    – partial (contains) filter by location, matches on every letter typed
      ?ordering=created_at – explicit sort (default is already -created_at)
      ?page=<n>            – page number (10 results per page)
    """
    queryset = JobPosting.objects.all().order_by('-created_at')
    serializer_class = JobPostingSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = JobPostingFilter              # ?location=Rem → matches "Remote"
    search_fields = ['title', 'description']       # ?search=python
    ordering_fields = ['created_at']
    ordering = ['-created_at']                     # Default: newest first


class JobPostingDetailView(generics.RetrieveAPIView):
    """
    GET /api/jobs/<id>/

    Returns a single job posting.
    Same field-level masking applies based on the requester's membership tier.
    """
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [AllowAny]
