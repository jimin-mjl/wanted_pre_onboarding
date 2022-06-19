from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker

from .factories import CompanyFactory, PostFactory, UserFactory
from .models import Post

faker = Faker()


class PostListCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.company = CompanyFactory.create()
        self.post1 = PostFactory.create(company=self.company)
        self.post2 = PostFactory.create(company=self.company)

    def test_list(self):
        """채용공고 목록 페이지 API 테스트"""
        url = reverse("jobs:list")
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], Post.objects.count())

    def test_search_by_keywords(self):
        """채용공고 검색 기능 테스트"""
        url = reverse("jobs:list") + f"?search={self.post1.company.name[:3]}"
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(self.post1.id, [result["id"] for result in res.data["results"]])

    def test_create(self):
        """채용공고 생성 API 테스트"""
        url = reverse("jobs:list")
        count = Post.objects.count()
        data = {
            "company": self.company.id,
            "title": faker.name(),
            "position": faker.job(),
            "compensation": faker.pyint(),
        }
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), count + 1)


class PostRetrieveUpdateDestroyAPIViewTestCase(APITestCase):
    def setUp(self):
        self.company = CompanyFactory.create()
        self.post = PostFactory.create(company=self.company)
        self.related_post = PostFactory.create(company=self.company)

    def test_retrieve(self):
        """채용공고 상세 페이지 API 테스트"""
        url = reverse("jobs:detail", kwargs={"pk": self.post.id})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(self.related_post.id, res.data["related_posts"])

    def test_update(self):
        """채용공고 수정 API 테스트"""
        url = reverse("jobs:detail", kwargs={"pk": self.post.id})
        prev_title = self.post.title
        prev_position = self.post.position
        data = {
            "title": prev_title + " modified",
            "position": prev_position + " modified",
        }
        res = self.client.patch(url, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.data["title"], prev_title)
        self.assertNotEqual(res.data["position"], prev_position)

    def test_delete(self):
        """채용공고 삭제 API 테스트"""
        url = reverse("jobs:detail", kwargs={"pk": self.post.id})
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(self.post, Post.objects.all())


class JobApplyAPIViewTestCase(APITestCase):
    def setUp(self):
        self.company = CompanyFactory.create()
        self.post = PostFactory.create(company=self.company)
        self.user = UserFactory.create()
        self.client.force_login(user=self.user)

    def test_apply(self):
        """채용공고 지원 API 테스트"""
        url = reverse("jobs:application", kwargs={"pk": self.post.id})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(self.user, self.post.applicants.all())

    def test_apply_twice(self):
        """중복 지원 제한 기능 동작 테스트"""
        url = reverse("jobs:application", kwargs={"pk": self.post.id})
        self.post.applicants.add(self.user)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
