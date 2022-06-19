from django.urls import path

from .views import (
    PostListCreateAPIView,
    PostRetrieveUpdateDestroyAPIView,
    job_apply_api_view,
)

app_name = "jobs"

urlpatterns = [
    path("", PostListCreateAPIView.as_view(), name="list"),
    path("<int:pk>/", PostRetrieveUpdateDestroyAPIView.as_view(), name="detail"),
    path("<int:pk>/application/", job_apply_api_view, name="application"),
]
