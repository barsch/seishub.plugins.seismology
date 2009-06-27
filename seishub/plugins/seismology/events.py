# -*- coding: utf-8 -*-
"""
Seismology package for SeisHub.
"""

from seishub.core import Component, implements
from seishub.packages.interfaces import IAdminPanel
import os


class EventsPanel(Component):
    """
    """
    implements(IAdminPanel)

    template = 'templates' + os.sep + 'events.tmpl'
    panel_ids = ('seismology', 'Seismology', 'events', 'Events')

    def render(self, request):
        data = {}
        return data
