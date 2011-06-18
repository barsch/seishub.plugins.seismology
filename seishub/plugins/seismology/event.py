# -*- coding: utf-8 -*-
"""
Event panels and mappers.
"""

from obspy.core import UTCDateTime
from seishub.core.core import Component, implements
from seishub.core.db.util import formatResults
from seishub.core.packages.interfaces import IMapper, IAdminPanel
from sqlalchemy import Table, sql
import os


class EventPanel(Component):
    """
    A seismic event overview for the administrative web interface.
    """
    implements(IAdminPanel)

    template = 'templates' + os.sep + 'events.tmpl'
    panel_ids = ('seismology', 'Seismology', 'events', 'Events')

    def render(self, request): #@UnusedVariable
        data = {}
        return data


class EventListMapper(Component):
    """
    Generates a list of available seismic events.
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
        except:
            limit = 50
        # restrict maximal number of events to 2500
        offset = int(request.args0.get('offset', 0))
        # build up query
        query = sql.select([tab])
        # process arguments
        # this is a string value, it returns None if nothing is given
        for key in ['localisation_method', 'account', 'user']:
            temp = request.args0.get(key)
            if temp:
                query = query.where(tab.c[key] == temp)
        # min-max datetime values
        for key in ['datetime', 'first_pick', 'last_pick']:
            try:
                temp = UTCDateTime(request.args0.get(key))
                query = query.where(tab.c[key] == temp.datetime)
            except:
                pass
            try:
                temp = UTCDateTime(request.args0.get('min_' + key))
                query = query.where(tab.c[key] >= temp.datetime)
            except:
                pass
            try:
                temp = UTCDateTime(request.args0.get('max_' + key))
                query = query.where(tab.c[key] <= temp.datetime)
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
        # min-max integer values
        for key in ['used_p', 'used_s']:
            try:
                temp = int(request.args0.get(key))
                query = query.where(tab.c[key] == temp)
            except:
                pass
            try:
                temp = int(request.args0.get('min_' + key))
                query = query.where(tab.c[key] >= temp)
            except:
                pass
            try:
                temp = int(request.args0.get('max_' + key))
                query = query.where(tab.c[key] <= temp)
            except:
                pass
        # execute query
        results = request.env.db.query(query.offset(offset).limit(limit))
        # ok count all distinct values
        query = sql.select([sql.func.count(tab.c['document_id'].distinct())])
        # execute query
        try:
            count = request.env.db.query(query).fetchone()[0]
        except:
            count = 0
        return formatResults(request, results, limit=limit, offset=offset,
                             count=count)


class BeachballMapper(Component):
    """
    Returns a beachball image for the given parameters.
    """
    implements(IMapper)

    package_id = 'seismology'
    mapping_url = '/seismology/event/plotBeachball'

    def process_GET(self, request):
        from obspy.imaging.beachball import Beachball
        # parse input arguments
        try:
            fm = request.args0.get('fm', '235, 80, 35')
            size = int(request.args0.get('size', 100))
            alpha = float(request.args0.get('alpha', 0.8))
            linewidth = float(request.args0.get('linewidth', 2))
            # try to parse fm
            if fm.count(',') == 2:
                fm = fm.split(',')
                fm = [float(fm[0]), float(fm[1]), float(fm[2])]
            elif fm.count(',') == 5:
                fm = fm.split(',')
                fm = [float(fm[0]), float(fm[1]), float(fm[2]),
                      float(fm[3]), float(fm[4]), float(fm[5])]
            else:
                return ''
        except:
            return ''
        if alpha < 0 or alpha > 1:
            alpha = 1
        if linewidth < 0 or linewidth > 10:
            linewidth = 2
        if size < 100 or size > 1000:
            size = 100
        # generate correct header
        request.setHeader('content-type', 'image/svg+xml; charset=UTF-8')
        # create beachball
        return Beachball(fm, size, format='svg', alpha=alpha,
                         linewidth=linewidth)
