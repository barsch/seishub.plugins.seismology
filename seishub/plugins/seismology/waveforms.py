# -*- coding: utf-8 -*-
"""
Seismology package for SeisHub.
"""

from obspy.core.util import UTCDateTime
from obspy.mseed import libmseed
from seishub.core import Component, implements
from seishub.db.util import querySingleColumn, formatResults
from seishub.packages.interfaces import IAdminPanel, IMapper
from seishub.registry.defaults import miniseed_tab
from sqlalchemy import sql
import datetime
import os


class WaveformsPanel(Component):
    """
    """
    implements(IAdminPanel)

    template = 'templates' + os.sep + 'waveforms.tmpl'
    panel_ids = ('seismology', 'Seismology', 'waveforms', 'Waveforms')

    def render(self, request):
        data = {}
        return data


class WaveformNetworkIDMapper(Component):
    """
    Fetches all possible network id's.
    """
    implements(IMapper)

    mapping_url = '/seismology/waveform/getNetworkIds'

    def process_GET(self, request):
        return querySingleColumn(request, 'default_miniseed', 'network_id')


class WaveformStationIDMapper(Component):
    """
    Fetches all possible station id's.
    """
    implements(IMapper)

    mapping_url = '/seismology/waveform/getStationIds'

    def process_GET(self, request):
        kwargs = {}
        kwargs['network_id'] = request.args0.get('network_id', None)
        return querySingleColumn(request, 'default_miniseed', 'station_id',
                                 **kwargs)


class WaveformLocationIDMapper(Component):
    """
    Fetches all possible location id's.
    """
    implements(IMapper)

    mapping_url = '/seismology/waveform/getLocationIds'

    def process_GET(self, request):
        kwargs = {}
        kwargs['network_id'] = request.args0.get('network_id', None)
        kwargs['station_id'] = request.args0.get('station_id', None)
        return querySingleColumn(request, 'default_miniseed', 'location_id',
                                 **kwargs)


class WaveformChannelIDMapper(Component):
    """
    Fetches all possible channel id's.
    """
    implements(IMapper)

    mapping_url = '/seismology/waveform/getChannelIds'

    def process_GET(self, request):
        kwargs = {}
        kwargs['network_id'] = request.args0.get('network_id', None)
        kwargs['station_id'] = request.args0.get('station_id', None)
        kwargs['location_id'] = request.args0.get('location_id', None)
        return querySingleColumn(request, 'default_miniseed', 'channel_id',
                                 **kwargs)


class WaveformLatencyMapper(Component):
    """
    Generates a list of latency values for each channel.
    """
    implements(IMapper)

    mapping_url = '/seismology/waveform/getLatency'

    def process_GET(self, request):
        # process parameters
        columns = [
            miniseed_tab.c['network_id'], miniseed_tab.c['station_id'],
            miniseed_tab.c['location_id'], miniseed_tab.c['channel_id'],
            (datetime.datetime.utcnow() -
             sql.func.max(miniseed_tab.c['end_datetime'])).label('latency')]
        group_by = [
            miniseed_tab.c['network_id'], miniseed_tab.c['station_id'],
            miniseed_tab.c['location_id'], miniseed_tab.c['channel_id']]
        # build up query
        query = sql.select(columns, group_by=group_by, order_by=group_by)
        for col in ['network_id', 'station_id', 'location_id', 'channel_id']:
            text = request.args0.get(col, None)
            if not text:
                continue
            if '*' in text or '?' in text:
                text = text.replace('?', '_')
                text = text.replace('*', '%')
                query = query.where(miniseed_tab.c[col].like(text))
            else:
                query = query.where(miniseed_tab.c[col] == text)
        # execute query
        try:
            results = request.env.db.query(query)
        except:
            results = []
        return formatResults(request, results)


class WaveformCutterMapper(Component):
    """
    """
    implements(IMapper)

    mapping_url = '/seismology/waveform/getWaveform'

    def process_GET(self, request):
        # process parameters
        try:
            start = request.args0.get('start_datetime')
            start = UTCDateTime(start)
        except:
            start = UTCDateTime()
        try:
            end = request.args0.get('end_datetime')
            end = UTCDateTime(end)
        except:
            # 10 minutes
            end = start + (60 * 10)
        # limit time span to maximal 6 hours
        if end - start > 60 * 60 * 6:
            end = start + 60 * 60 * 6
        # build up query
        columns = [miniseed_tab.c['path'], miniseed_tab.c['file']]
        query = sql.select(columns)
        for col in ['network_id', 'station_id', 'location_id', 'channel_id']:
            text = request.args0.get(col, None)
            if not text:
                continue
            if '*' in text or '?' in text:
                text = text.replace('?', '_')
                text = text.replace('*', '%')
                query = query.where(miniseed_tab.c[col].like(text))
            else:
                query = query.where(miniseed_tab.c[col] == text)
        query = query.where(miniseed_tab.c['end_datetime'] > start.datetime)
        query = query.where(miniseed_tab.c['start_datetime'] < end.datetime)
        # execute query
        try:
            results = request.env.db.query(query).fetchall()
        except:
            results = []
        file_list = []
        for result in results:
            file_list.append(result[0] + os.sep + result[1])
        ms = libmseed()
        data = ms.mergeAndCutMSFiles(file_list, start, end)
        # generate correct header
        request.setHeader('content-type', 'binary/octet-stream')
        return data


