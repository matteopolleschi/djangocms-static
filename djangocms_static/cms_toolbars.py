from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse
from django.urls import reverse
# from django.core.urlresolvers import reverse
# from polls.models import Poll


class StaticGeneratorToolbar(CMSToolbar):

    def populate(self):
        menu = self.toolbar.get_or_create_menu(
            'static-site-generator',
            'Static',
            )
        menu.add_sideframe_item(
            name='Generate static version',                              # name of the new menu item
            url=reverse('generate'),    # the URL it should open with
        )


toolbar_pool.register(StaticGeneratorToolbar)
