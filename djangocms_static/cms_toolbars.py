from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from cms.constants import RIGHT
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse


class StaticGeneratorToolbar(CMSToolbar):

    def populate(self):
        buttonlist = self.toolbar.add_button_list(position=10, side=RIGHT)
        buttonlist.add_modal_button(
            name=_('Create static site'),
            url=reverse('generate'),
        )


toolbar_pool.register(StaticGeneratorToolbar)
