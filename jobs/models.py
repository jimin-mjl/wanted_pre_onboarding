from django.db import models
from django.contrib.auth import get_user_model


class TimeStampedModel(models.Model):
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True)
    updated_datetime = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True
        ordering = ("-created_datetime",)


class Company(TimeStampedModel):
    name = models.CharField("회사명", max_length=255)
    country = models.CharField("국가", max_length=255, default="", blank=True)
    region = models.CharField("회사 소재지", max_length=255, default="", blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Post(TimeStampedModel):
    company = models.ForeignKey(
        "Company", verbose_name="회사", related_name="posts", on_delete=models.CASCADE
    )
    applicants = models.ManyToManyField(
        get_user_model(), verbose_name="지원자 목록", related_name="applied_posts"
    )

    title = models.CharField("제목", max_length=255)
    description = models.TextField("상세 채용정보", default="", blank=True)
    position = models.CharField("포지션", max_length=255, default="", blank=True)
    compensation = models.IntegerField("채용 보상금", default=0, blank=True)
    technology = models.CharField("사용기술", max_length=255, default="", blank=True)
    deadline = models.DateTimeField("마감일", null=True, blank=True)

    def __str__(self):
        return self.title
