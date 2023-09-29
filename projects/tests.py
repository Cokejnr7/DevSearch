from django.test import TestCase
from django.urls import reverse, resolve
from . import views

# Create your tests here.


class TestUrls(TestCase):
    def test_project_list_url_resolves(self):
        url = reverse("projects")
        self.assertEqual(resolve(url).func, views.project)

    def test_project_url_resolves(self):
        url = reverse("project", args=[1])
        self.assertEqual(resolve(url).func, views.singleProject)

    def test_project_create_url_resolves(self):
        url = reverse("create-project")
        self.assertEqual(resolve(url).func, views.create)

    def test_project_update_url_resolves(self):
        url = reverse("update-project", args=[1])
        self.assertEqual(resolve(url).func, views.update)
