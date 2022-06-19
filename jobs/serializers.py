from django.utils import timezone

from rest_framework import serializers

from .models import Post


class PostBaseSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField(label="회사명")
    country = serializers.SerializerMethodField(label="국가")
    region = serializers.SerializerMethodField(label="지역")

    class Meta:
        model = Post
        fields = (
            "id",
            "company",
            "company_name",
            "title",
            "description",
            "position",
            "compensation",
            "technology",
            "country",
            "region",
            "deadline",
        )
        read_only_fields = ("company_name", "country", "region")

    def get_company_name(self, obj):
        return obj.company.name

    def get_country(self, obj):
        return obj.company.country

    def get_region(self, obj):
        return obj.company.region


class PostListSerializer(PostBaseSerializer):
    pass


class PostDetailSerializer(PostBaseSerializer):
    related_posts = serializers.SerializerMethodField(label="연관 채용공고")

    class Meta(PostBaseSerializer.Meta):
        fields = (
            "id",
            "company",
            "company_name",
            "title",
            "description",
            "position",
            "compensation",
            "technology",
            "country",
            "region",
            "created_datetime",
            "deadline",
            "related_posts",
        )
        read_only_fields = ("company_name", "country", "region", "company")

    def get_related_posts(self, obj):
        qs = obj.company.posts.exclude(id=obj.id).exclude(deadline__lte=timezone.now())
        return qs.values_list("id", flat=True)
