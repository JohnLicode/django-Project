from django.contrib import admin
from django.urls import path
from studentorg.views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel route
    path('', HomePageView.as_view(), name='home'),  # Home page route
]
