# -*- coding: utf-8 -*-
"""
Seismology package for SeisHub.
"""

from obspy.core import UTCDateTime
from seishub.core import Component, implements
from seishub.db.util import formatResults
from seishub.packages.interfaces import IMapper
from sqlalchemy import Table, sql


#class EventPanel(Component):
#    """
#    """
#    implements(IAdminPanel)
#
#    template = 'templates' + os.sep + 'events.tmpl'
#    panel_ids = ('seismology', 'Seismology', 'events', 'Events')
#
#    def render(self, request):
#        data = {}
#        return data


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
        # this is a string value, it returns None if nothing is given
        temp = request.args0.get('localisation_method')
        if temp:
            query = query.where(tab.c['localisation_method'] == temp)
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
