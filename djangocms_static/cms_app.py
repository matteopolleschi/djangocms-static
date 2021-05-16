from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import gettext_lazy as _


@apphook_pool.register  # register the application
class StaticGeneratorApphook(CMSApp):
    app_name = 'djangocms_static'
    name = _("Static Site Generator")
    urls = ["djangocms_static.urls"]

    def get_urls(self, page=None, language=None, **kwargs):
        return ["djangocms_static.urls"]


apphook_pool.register(StaticGeneratorApphook)
