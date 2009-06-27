# -*- coding: utf-8 -*-
"""
Seismology package for SeisHub.
"""

from seishub.core import Component, implements
from seishub.packages.interfaces import IAdminPanel, IMapper
from seishub.db.util import querySingleColumn
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


