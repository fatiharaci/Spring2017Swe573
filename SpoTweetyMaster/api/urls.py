from django.conf.urls import url
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = {
    url(r'api/$', views.api_view)
}

urlpatterns = format_suffix_patterns(urlpatterns)
