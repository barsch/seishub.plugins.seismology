# -*- coding: utf-8 -*-
"""
Seismology package for SeisHub.
"""

from obspy.core.util import UTCDateTime
from seishub.core import Component, implements
from seishub.db.util import formatResults
from seishub.packages.interfaces import IAdminPanel, IMapper
from sqlalchemy import Table, sql
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


class EventListMapper(Component):
    """
    """
    implements(IMapper)

    package_id = 'seismology'
    mapping_url = '/seismology/event/getList'

    def process_GET(self, request):
        tab = Table('/seismology/event', request.env.db.metadata,
                    autoload=True)
        # fetch arguments
        try:
            limit = int(request.args0.get('limit'))
            offset = int(request.args0.get('offset', 0))
        except:
            limit = None
            offset = 0
        oncl = sql.and_(1 == 1)
        # build up query
        query = sql.select([tab], oncl, limit=limit, offset=offset)
        # process arguments
        try:
            temp = UTCDateTime(request.args0.get('datetime'))
            query = query.where(tab.c['datetime'] == temp.datetime)
        except:
            pass
        try:
            temp = UTCDateTime(request.args0.get('min_datetime'))
            query = query.where(tab.c['datetime'] >= temp.datetime)
        except:
            pass
        try:
            temp = UTCDateTime(request.args0.get('max_datetime'))
            query = query.where(tab.c['datetime'] <= temp.datetime)
        except:
            pass
        # min-max float values
        for key in ['latitude', 'longitude', 'magnitude', 'depth']:
            try:
                temp = float(request.args0.get(key))
                query = query.where(tab.c[key] == temp)
            except:
                pass
            try:
                temp = float(request.args0.get('min_' + key))
                query = query.where(tab.c[key] >= temp)
            except:
                pass
            try:
                temp = float(request.args0.get('max_' + key))
                query = query.where(tab.c[key] <= temp)
            except:
                pass
        # execute query
        try:
            results = request.env.db.query(query)
        except:
            results = []
        # ok count all distinct values
        query = sql.select([sql.func.count(tab.c['document_id'].distinct())])
        # execute query
        try:
            count = request.env.db.query(query).fetchone()[0]
        except:
            count = 0
        return formatResults(request, results, limit=limit, offset=offset,
                             count=count)
