"""python_blog_scraping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articlesByReleaseDate/<str:articleReleaseDate>/', views.GetArticlesByReleaseDate.as_view()),
    path('extractArticlesByReleaseDate/', views.ExtractBlogByReleaseDate.as_view()),
    path('extractArticlesByReleaseDate/<str:extractionRequestId>/', views.ExtractBlogByReleaseDate.as_view()),
    path('python_blog_scraping/<int:job_id>', views.python_blog_scraping, name="scraping")
]

"""
curl -X POST "http://0.0.0.0:8000/extractArticlesByReleaseDate/?articleReleaseStartDate=2022-09-04&articleReleaseEndDate=2022-09-04" -H  "accept: application/json" -d ""
"""