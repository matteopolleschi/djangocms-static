"""Views to manage the static sites."""
import os

from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _

from cms.views import details
from cms.models.pagemodel import Page
from cms.page_rendering import render_page


BASE_DIR = Path(__file__).resolve().parent

STORAGE_SLUG = 'static_sites'

STORAGE_PATH = os.path.join(BASE_DIR, STORAGE_SLUG)


def get_path(url):
    rel_path = STORAGE_SLUG
    for directory in url.strip('/').split('/'):
        full_path = os.path.join(BASE_DIR, rel_path, directory)
        if os.path.exists(full_path):
            pass
        else:
            print('no existeix {}'.format(os.path.join(rel_path, directory)))
            os.mkdir(full_path)
        rel_path += '/{}'.format(directory)
    return url.strip('/')


def create_html_files(request):
    cms_pages = Page.objects.filter(publication_date__isnull=False)
    request.user = AnonymousUser()
    log = []
    done = []
    for page in cms_pages:
        languages = page.get_languages()
        for language in languages:
            url = page.get_public_url(language)
            if url not in done:
                slug = page.get_slug()
                done.append(url)
                path = get_path(url)
                request.path = path
                request.path_info = path
                request.current_page = page
                request.toolbar.show_toolbar = False
                if page.is_home:
                    template = details(request, '')
                else:
                    template = details(request, slug)
                content = ''
                if hasattr(template, 'render'):
                    content = template.render().content
                else:
                    content = template.content

                content = content.decode("utf-8")

                with open(path, 'w') as file:
                    file.write(content)

                log.append('<a href="file://{}" target="_blank">{}</a>'.format(
                    path, _("Review local copy of {}.html".format(page_name))
                ))
    response = '<div style="height: 100px;"></div>'
    response += '<h4>Pages created</h4>'
    response += 'Location: {}<br>'.format(STORAGE_PATH)
    response += "<br>".join(log)
    return HttpResponse(response)
