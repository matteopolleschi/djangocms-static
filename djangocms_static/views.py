"""Views to manage the static sites."""
import os
import shutil

import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from cms.models.pagemodel import Page

STORAGE_SLUG = 'static_sites'

STORAGE_PATH = os.path.join(settings.BASE_DIR, STORAGE_SLUG)

if hasattr(settings, 'STATIC_STORAGE_PATH'):
    STORAGE_PATH = settings.STATIC_STORAGE_PATH


class MissingStaticRoot(BaseException):
    pass


def make_dir(url):
    """Build the site tree directory."""
    parts = url.strip('/').split('/')
    done = []
    for part in parts:
        path = os.path.join(STORAGE_PATH, '/'.join(done), part)
        if not os.path.exists(path):
            os.mkdir(path)
        done.append(part)


class StaticSiteGenerator(TemplateView):
    """Static Site Generator main class."""

    template_name = "summary.html"

    def __init__(self, *args, **kwargs):
        """Constructor."""
        super().__init__(*args, **kwargs)
        self.done = []
        self.SOURCE_DOMAIN = None

    def setup(self, request, *args, **kwargs):
        """Initialize."""
        super().setup(request, *args, **kwargs)
        if not os.path.exists(STORAGE_PATH):
            os.mkdir(STORAGE_PATH)
        if request.is_secure():
            self.SOURCE_DOMAIN = 'https://{}'.format(request.get_host())
        else:
            self.SOURCE_DOMAIN = 'http://{}'.format(request.get_host())

    def dispatch(self, request, *args, **kwargs):
        """Create and save the HTML files for the site pages."""
        try:
            self.copy_static_resources()
        except MissingStaticRoot:
            self.template_name = 'general_error.html'
            kwargs['error'] = _('There is no STATIC_ROOT defined in the settings file')
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            self.template_name = 'general_error.html'
            kwargs['error'] = str(e)
            return super().dispatch(request, *args, **kwargs)
        cms_pages = Page.objects.filter(publication_date__isnull=False)
        for page in cms_pages:
            languages = page.get_languages()
            for language in languages:
                url = page.get_public_url(language)
                if url not in self.done:
                    self.done.append(url)
                    static_page_path = '{}{}index.html'.format(STORAGE_PATH, url)
                    fetch_url = "{}{}".format(self.SOURCE_DOMAIN, url)
                    response = requests.get(fetch_url)
                    make_dir(url)
                    with open(static_page_path, 'w') as file:
                        file.write(response.text)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add the result to the output template."""
        context = super().get_context_data(**kwargs)
        context.update({
            'pages': self.done,
            'storage_path': STORAGE_PATH
        })
        return context

    def copy_static_resources(self):
        """Copy the static resources."""
        if not hasattr(settings, 'STATIC_ROOT'):
            raise MissingStaticRoot()
        destination = os.path.join(STORAGE_PATH, 'static')
        if os.path.exists(destination):
            shutil.rmtree(destination)
        shutil.copytree(settings.STATIC_ROOT, destination)
