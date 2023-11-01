from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import Post, User


def create_post(title, content, user):
    """
    Create a post

    Args:
        title (str): Post title
        content (str): Post detail
        user (User): An User object
    """
    return Post.objects.create(title=title, content=content, user=user)


def create_user(email, name, password):
    """
    Create a user with the given email, name and password.

    Args:
        email (str): User email
        name (str): User name
        password (str): User password
    """
    return User.objects.create(email=email, name=name, password=password)


class PostViewTests(TestCase):
    def test_no_posts(self):
        """
        If no posts exist, empty list is returned.
        """
        response = self.client.get(reverse("post-list"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.data["results"], [])

    def test_all_posts(self):
        """
        The count should be equal to the total number of posts.
        """
        user = create_user("preetam@gmail.com", "Preetam", "preetam@123")
        post1 = create_post("Title1", "This is first post", user)
        post2 = create_post("Title2", "This is second post", user)
        response = self.client.get(reverse("post-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)


class UserViewTests(TestCase):
    def test_user_registration(self):
        url = reverse("register")
        response = self.client.post(
            url,
            {
                "email": "preetam@gmail.com",
                "name": "Preetam",
                "password": "preetam@123",
            },
            format="json",
        )
        self.assertEqual(response.data["message"], "Registration Successful")

    def test_user_login(self):
        url = reverse("register")
        user_email = "preetam@gmail.com"
        user_name = "Preetam"
        user_password = "preetam@123"
        self.client.post(
            url,
            {"email": user_email, "name": user_name, "password": user_password},
            format="json",
        )

        url = reverse("login")
        response = self.client.post(
            url, {"email": user_email, "password": user_password}, format="json"
        )
        # print(response.data)
        self.assertEqual(response.data["message"], "Login Success")

    def test_authenticate_user_can_create_post(self):
        url = reverse("register")
        user_email = "preetam@gmail.com"
        user_name = "Preetam"
        user_password = "preetam@123"
        self.client.post(
            url,
            {"email": user_email, "name": user_name, "password": user_password},
            format="json",
        )

        url = reverse("login")
        response = self.client.post(
            url, {"email": user_email, "password": user_password}, format="json"
        )

        access_token = response.data["token"]["access"]

        create_post_url = reverse("post-list")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.client.post(
            create_post_url,
            {"title": "title1", "content": "content1"},
            headers=headers,
            format="json",
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_can_view_posts(self):
        url = reverse("register")
        user_email = "preetam@gmail.com"
        user_name = "Preetam"
        user_password = "preetam@123"
        self.client.post(
            url,
            {"email": user_email, "name": user_name, "password": user_password},
            format="json",
        )

        url = reverse("login")
        response = self.client.post(
            url, {"email": user_email, "password": user_password}, format="json"
        )

        access_token = response.data["token"]["access"]

        create_post_url = reverse("post-list")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.client.post(
            create_post_url,
            {"title": "title1", "content": "content1"},
            headers=headers,
            format="json",
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(
            create_post_url,
            {"title": "title2", "content": "content2"},
            headers=headers,
            format="json",
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        get_posts_url = reverse("post-list")
        response = self.client.get(get_posts_url, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_authenticated_user_can_view_single_post(self):
        url = reverse("register")
        user_email = "preetam@gmail.com"
        user_name = "Preetam"
        user_password = "preetam@123"
        self.client.post(
            url,
            {"email": user_email, "name": user_name, "password": user_password},
            format="json",
        )

        url = reverse("login")
        response = self.client.post(
            url, {"email": user_email, "password": user_password}, format="json"
        )

        access_token = response.data["token"]["access"]

        create_post_url = reverse("post-list")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.client.post(
            create_post_url,
            {"title": "title1", "content": "content1"},
            headers=headers,
            format="json",
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post_1_id = response.data["id"]
        response = self.client.post(
            create_post_url,
            {"title": "title2", "content": "content2"},
            headers=headers,
            format="json",
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        get_posts_url = reverse("post-detail", args=(post_1_id,))
        response = self.client.get(get_posts_url, format="json")
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_unauthenticate_user_can_not_create_post(self):
        create_post_url = reverse("post-list")
        response = self.client.post(
            create_post_url, {"title": "title1", "content": "content1"}, format="json"
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_unauthenticated_user_can_view_posts(self):
    # def test_unauthenticated_user_can_view_single_post(self):

    # def test_owner_can_update_post(self):
    # def test_owner_can_delete_post(self):

    # def test_different_user_can_not_update_post(self):
    # def test_different_user_can_not_delete_post(self):

    # def test_unauthenticated_user_can_not_update_post(self):
    # def test_unauthenticated_user_can_not_delete_post(self):
