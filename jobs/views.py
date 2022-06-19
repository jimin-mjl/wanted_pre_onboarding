from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import PostListSerializer, PostDetailSerializer
from .models import Post


class PostListCreateAPIView(ListCreateAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.select_related("company").all()
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        "title",
        "position",
        "description",
        "technology",
        "company__name",
        "company__country",
        "company__region",
    )


class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.select_related("company").all()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def job_apply_api_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    user = request.user
    is_duplicated = bool(post.applicants.filter(id=user.id))

    if is_duplicated:  # 중복 지원 제한
        return Response(
            {"result": "fail", "detail": "Duplicated Application"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    post.applicants.add(user)
    return Response({"result": "success"})
