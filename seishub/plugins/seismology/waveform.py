# -*- coding: utf-8 -*-
"""
Seismology package for SeisHub.
"""

from lxml.etree import Element, SubElement as Sub
from obspy.core import UTCDateTime
from obspy.db.db import WaveformChannel, WaveformFile, WaveformPath
from seishub.core import Component, implements
from seishub.db.util import formatORMResults
from seishub.exceptions import InternalServerError
from seishub.packages.interfaces import IMapper, IAdminPanel
from seishub.util.xmlwrapper import toString
from sqlalchemy import func, Column
import os


class WaveformPanel(Component):
    """
    A waveform overview for the administrative web interface.
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
        session = self.env.db.session()
        query = session.query(WaveformChannel.network)
        query = query.distinct()
        return formatORMResults(request, query)


class WaveformStationIDMapper(Component):
    """
    Fetches all possible station id's.
    """
    implements(IMapper)

    mapping_url = '/seismology/waveform/getStationIds'

    def process_GET(self, request):
        network = request.args0.get('network_id', None)
        session = self.env.db.session()
        query = session.query(WaveformChannel.station)
        query = query.distinct()
        if network:
            query = query.filter(WaveformChannel.network == network)
        return formatORMResults(request, query)


class WaveformLocationIDMapper(Component):
    """
    Fetches all possible location id's.
    """
    implements(IMapper)

    mapping_url = '/seismology/waveform/getLocationIds'

    def process_GET(self, request):
        network = request.args0.get('network_id', None)
        station = request.args0.get('station_id', None)
        session = self.env.db.session()
        query = session.query(WaveformChannel.location)
        query = query.distinct()
        if network:
            query = query.filter(WaveformChannel.network == network)
        if station:
            query = query.filter(WaveformChannel.station == station)
        return formatORMResults(request, query)


class WaveformChannelIDMapper(Component):
    """
    Fetches all possible channel id's.
    """
    implements(IMapper)

    mapping_url = '/seismology/waveform/getChannelIds'

    def process_GET(self, request):
        network = request.args0.get('network_id', None)
        station = request.args0.get('station_id', None)
        location = request.args0.get('location_id', None)
        session = self.env.db.session()
        query = session.query(WaveformChannel.channel)
        query = query.distinct()
        if network:
            query = query.filter(WaveformChannel.network == network)
        if station:
            query = query.filter(WaveformChannel.station == station)
        if location:
            query = query.filter(WaveformChannel.location == location)
        return formatORMResults(request, query)


class WaveformLatencyMapper(Component):
    """
    Generates a list of latency values for each channel.
    """
    implements(IMapper)

    mapping_url = '/seismology/waveform/getLatency'

    def process_GET(self, request):
        # build up query
        session = self.env.db.session()
        query = session.query(
            WaveformChannel.network, WaveformChannel.station,
            WaveformChannel.location, WaveformChannel.channel,
            func.max(WaveformChannel.endtime).label('latency')
        )
        query = query.group_by(
            WaveformChannel.network, WaveformChannel.station,
            WaveformChannel.location, WaveformChannel.channel
        )
        # process arguments
        for key in ['network_id', 'station_id', 'location_id', 'channel_id']:
            text = request.args0.get(key, None)
            if text == None:
                continue
            col = getattr(WaveformChannel, key[:-3])
            if text == "":
                query = query.filter(col == None)
            elif '*' in text or '?' in text:
                text = text.replace('?', '_')
                text = text.replace('*', '%')
                query = query.filter(col.like(text))
            else:
                query = query.filter(col == text)
        return formatORMResults(request, query)


class WaveformPathMapper(Component):
    """
    Generates a list of available waveform files.
    """
    implements(IMapper)

    mapping_url = '/seismology/waveform/getWaveformPath'

    def process_GET(self, request):
        # build up query
        session = self.env.db.session()
        query = session.query(WaveformPath.path,
                              WaveformFile.file,
                              WaveformChannel.network,
                              WaveformChannel.station,
                              WaveformChannel.location,
                              WaveformChannel.channel)
        query = query.filter(WaveformPath.id == WaveformFile.path_id)
        query = query.filter(WaveformFile.id == WaveformChannel.file_id)
        # process arguments
        for key in ['network_id', 'station_id', 'location_id', 'channel_id']:
            text = request.args0.get(key, None)
            if text == None:
                continue
            col = getattr(WaveformChannel, key[:-3])
            if text == "":
                query = query.filter(col == None)
            elif '*' in text or '?' in text:
                text = text.replace('?', '_')
                text = text.replace('*', '%')
                query = query.filter(col.like(text))
            else:
                query = query.filter(col == text)
        # start and end time
        try:
            start = request.args0.get('start_datetime')
            start = UTCDateTime(start)
        except:
            start = UTCDateTime() - 60 * 20
        finally:
            query = query.filter(WaveformChannel.endtime > start.datetime)
        try:
            end = request.args0.get('end_datetime')
            end = UTCDateTime(end)
        except:
            # 10 minutes
            end = UTCDateTime()
        finally:
            query = query.filter(WaveformChannel.starttime < end.datetime)
        # execute query
        file_dict = {}
        for result in query:
            fname = result[0] + os.sep + result[1]
            key = '%s.%s.%s.%s' % (result[2], result[3], result[4], result[5])
            file_dict.setdefault(key, []).append(fname)
        # return as xml resource
        xml = Element("query")
        for _i in file_dict.keys():
            s = Sub(xml, "channel", id=_i)
            for _j in file_dict[_i]:
                t = Sub(s, "file")
                t.text = _j
        return toString(xml)


class WaveformCutterMapper(Component):
    """
    Returns a requested waveform.
    """
    implements(IMapper)

    mapping_url = '/seismology/waveform/getWaveform'

    def process_GET(self, request):
        # build up query
        session = self.env.db.session()
        query = session.query(WaveformPath.path,
                              WaveformFile.file,
                              WaveformChannel.network,
                              WaveformChannel.station,
                              WaveformChannel.location,
                              WaveformChannel.channel)
        query = query.filter(WaveformPath.id == WaveformFile.path_id)
        query = query.filter(WaveformFile.id == WaveformChannel.file_id)
        # process arguments
        for key in ['network_id', 'station_id', 'location_id', 'channel_id']:
            text = request.args0.get(key, None)
            if text == None:
                continue
            col = getattr(WaveformChannel, key[:-3])
            if text == "":
                query = query.filter(col == None)
            elif '*' in text or '?' in text:
                text = text.replace('?', '_')
                text = text.replace('*', '%')
                query = query.filter(col.like(text))
            else:
                query = query.filter(col == text)
        # start and end time
        try:
            start = request.args0.get('start_datetime')
            start = UTCDateTime(start)
        except:
            start = UTCDateTime() - 60 * 20
        finally:
            query = query.filter(WaveformChannel.endtime > start.datetime)
        try:
            end = request.args0.get('end_datetime')
            end = UTCDateTime(end)
        except:
            # 10 minutes
            end = UTCDateTime()
        finally:
            query = query.filter(WaveformChannel.starttime < end.datetime)
        # execute query
        results = query.all()
        # check for results
        if len(results) == 0:
            # ok lets use arclink
            return self._fetchFromArclink(request, start, end)
        # get from local waveform archive
        from obspy.mseed.libmseed import LibMSEED
        ms = LibMSEED()
        file_dict = {}
        for result in results:
            fname = result[0] + os.sep + result[1]
            key = '%s.%s.%s.%s' % (result[2], result[3], result[4], result[5])
            file_dict.setdefault(key, []).append(fname)
        data = ''
        for id in file_dict.keys():
            data += ms.mergeAndCutMSFiles(file_dict[id], start, end)
        # generate correct header
        request.setHeader('content-type', 'binary/octet-stream')
        # disable content encoding like packing!
        request.received_headers["accept-encoding"] = ""
        return data

    def _fetchFromArclink(self, request, start, end):
        """
        """
        try:
            from obspy.arclink.client import Client
        except:
            return ''
        c = Client()
        # parameters
        nid = request.args0.get('network_id')
        sid = request.args0.get('station_id')
        lid = request.args0.get('location_id', '')
        cid = request.args0.get('channel_id', '*')
        try:
            st = c.getWaveform(nid, sid, lid, cid, start, end)
        except Exception, e:
            raise InternalServerError(e)
        # merge + cut
        #st.merge()
        st.trim(start, end)
        # write to arclink directory for request
        rpath = os.path.join(self.env.getSeisHubPath(), 'data', 'arclink')
        rfile = os.path.join(rpath, 'request%d' % UTCDateTime().timestamp)
        # XXX: args have to create temp files .... issue with obspy.mseed, or
        # actually issue with ctypes not accepting StringIO as filehandler ...
        st.write(rfile, format='MSEED')
        # write to arclink directory
        for tr in st:
            # network directory
            path = os.path.join(rpath, tr.stats.network)
            self._checkPath(path)
            # station directory
            path = os.path.join(path, tr.stats.station)
            self._checkPath(path)
            # channel directory
            path = os.path.join(path, tr.stats.channel)
            self._checkPath(path)
            file = tr.getId() + '.%d.%d.mseed' % (tr.stats.starttime.timestamp,
                                                  tr.stats.endtime.timestamp)
            tr.write(os.path.join(path, file), format='MSEED')
        # generate correct header
        request.setHeader('content-type', 'binary/octet-stream')
        # disable content encoding like packing!
        request.received_headers["accept-encoding"] = ""
        # XXX: again very ugly as not StringIO can be used ...
        fh = open(rfile, 'rb')
        data = fh.read()
        fh.close()
        os.remove(rfile)
        return data

    def _checkPath(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)


class WaveformPreviewMapper(Component):
    """
    Returns a requested waveform preview.
    """
    implements(IMapper)

    mapping_url = '/seismology/waveform/getWaveformPreview'

    def process_GET(self, request):
        # build up query
        session = self.env.db.session()
        query = session.query(WaveformChannel)
        # process arguments
        for key in ['network_id', 'station_id', 'location_id', 'channel_id']:
            text = request.args0.get(key, None)
            if text == None:
                continue
            col = getattr(WaveformChannel, key[:-3])
            if text == "":
                query = query.filter(col == None)
            elif '*' in text or '?' in text:
                text = text.replace('?', '_')
                text = text.replace('*', '%')
                query = query.filter(col.like(text))
            else:
                query = query.filter(col == text)
        # start and end time
        try:
            start = request.args0.get('start_datetime')
            start = UTCDateTime(start)
        except:
            start = UTCDateTime() - 60 * 20
        finally:
            query = query.filter(WaveformChannel.endtime > start.datetime)
        try:
            end = request.args0.get('end_datetime')
            end = UTCDateTime(end)
        except:
            # 10 minutes
            end = UTCDateTime()
        finally:
            query = query.filter(WaveformChannel.starttime < end.datetime)
        # execute query
        results = query.all()
        # create Stream
        from obspy.core import Stream
        st = Stream()
        for result in results:
            st.append(result.getPreview())
        #import pdb;pdb.set_trace()
        # merge and trim
        # XXX: fails yet!
        st.merge(fill_value=0)
        st.trim(start, end)
        # temporary file
        from obspy.core.util import NamedTemporaryFile
        temp = NamedTemporaryFile().name
        st.write(temp, format='MSEED')
        data = open(temp, 'rb').read()
        os.remove(temp)
        # generate correct header
        request.setHeader('content-type', 'binary/octet-stream')
        # disable content encoding like packing!
        request.received_headers["accept-encoding"] = ""
        return data
