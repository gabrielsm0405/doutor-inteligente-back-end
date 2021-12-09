"""health_cloud_back_end URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from health_cloud_back_end.app import views
from django.conf.urls.static import static
import os
from .settings import BASE_DIR

urlpatterns = [
    path('admin/', admin.site.urls),
    path("inference/", views.InferenceView.as_view({'post': 'makeInferece'})),
] + static("/images/", document_root=os.path.join(BASE_DIR, 'images'))
