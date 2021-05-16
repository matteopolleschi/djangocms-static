"""Routing URLs."""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from djangocms_static.views import create_html_files

admin.autodiscover()


urlpatterns = [
    path("generate/", create_html_files, name='generate'),
]
