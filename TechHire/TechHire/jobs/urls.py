from django.urls import path
from .views import JobPostingListView, JobPostingDetailView

urlpatterns = [
    path('jobs/', JobPostingListView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobPostingDetailView.as_view(), name='job-detail'),
]
