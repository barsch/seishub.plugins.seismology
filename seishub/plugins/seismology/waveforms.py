# -*- coding: utf-8 -*-
"""
Seismology package for SeisHub.
"""

from seishub.core import Component, implements
from seishub.db.util import querySingleColumn, formatResults
from seishub.packages.interfaces import IAdminPanel, IMapper
from seishub.registry.defaults import miniseed_tab
from sqlalchemy import sql, Column, DateTime
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
        network_id = request.args0.get('network_id', None)
        station_id = request.args0.get('station_id', None)
        location_id = request.args0.get('location_id', None)
        channel_id = request.args0.get('channel_id', None)
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
        if network_id:
            query = query.where(miniseed_tab.c['network_id'] == network_id)
        if station_id:
            query = query.where(miniseed_tab.c['station_id'] == station_id)
        if location_id:
            query = query.where(miniseed_tab.c['location_id'] == location_id)
        if channel_id:
            query = query.where(miniseed_tab.c['channel_id'] == channel_id)
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
        data = {}
        from obspy.mseed import libmseed
        ms = libmseed()
        #ms.mergeAndCutMSFiles(file_list, outfile, starttime, endtime)
        return data


