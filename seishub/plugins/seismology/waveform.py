# -*- coding: utf-8 -*-
"""
Waveform panels and mappers.
"""

from lxml.etree import Element, SubElement as Sub
from obspy.core import UTCDateTime, Stream, read
from obspy.core.preview import mergePreviews
from obspy.db.db import WaveformChannel, WaveformFile, WaveformPath
from obspy.gse2.libgse2 import ChksumError
from seishub.core.core import Component, implements
from seishub.core.db.util import formatORMResults, CustomJSONEncoder
from seishub.core.exceptions import InternalServerError
from seishub.core.packages.interfaces import IMapper, IAdminPanel, \
    IAdminStaticContent
from seishub.core.util.xmlwrapper import toString
from sqlalchemy import func, or_, and_
import numpy as np
import os
import pickle
import json


def _getPreview(session, **kwargs):
    # build up query
    query = session.query(WaveformChannel)
    # start and end time
    try:
        start = kwargs.get('start_datetime')
        start = UTCDateTime(start)
    except:
        start = UTCDateTime() - 60 * 20
    finally:
        query = query.filter(WaveformChannel.endtime > start.datetime)
    try:
        end = kwargs.get('end_datetime')
        end = UTCDateTime(end)
    except:
        # 10 minutes
        end = UTCDateTime()
    finally:
        query = query.filter(WaveformChannel.starttime < end.datetime)
    # process arguments
    if 'trace_ids' in kwargs:
        # filter over trace id list
        trace_ids = kwargs.get('trace_ids', '')
        trace_filter = or_()
        for trace_id in trace_ids.split(','):
            temp = trace_id.split('.')
            if len(temp) != 4:
                continue
            trace_filter.append(and_(
                WaveformChannel.network == temp[0],
                WaveformChannel.station == temp[1],
                WaveformChannel.location == temp[2],
                WaveformChannel.channel == temp[3]))
        if trace_filter.clauses:
            query = query.filter(trace_filter)
    else:
        # filter over network/station/location/channel id
        for key in ['network_id', 'station_id', 'location_id',
                    'channel_id']:
            text = kwargs.get(key, None)
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
    # execute query
    results = query.all()
    session.close()
    # create Stream
    st = Stream()
    for result in results:
        preview = result.getPreview()
        st.append(preview)
    # merge and trim
    st = mergePreviews(st)
    st.trim(start, end)
    return st, start, end


class WaveformPanel(Component):
    """
    A waveform overview for the administrative web interface.
    """
    implements(IAdminPanel, IAdminStaticContent)

    template = 'templates' + os.sep + 'waveforms.tmpl'
    panel_ids = ('seismology', 'Seismology', 'waveforms', 'Waveforms')

    def render(self, request): #@UnusedVariable
        data = {
        }
        return data

    def getStaticContent(self):
        path = os.path.join(os.path.dirname(__file__), 'statics',
                            'seisgram2k')
        return {'/seisgram2k': path}


class WaveformNetworkIDMapper(Component):
    """
    Fetches all possible network id's.
    """
    implements(IMapper)

    mapping_url = '/seismology/waveform/getNetworkIds'

    def process_GET(self, request):
        session = self.env.db.session()
        query = session.query(WaveformChannel.network)
        query = query.group_by(WaveformChannel.network)
        data = formatORMResults(request, query)
        session.close()
        return data


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
        if network:
            query = query.filter(WaveformChannel.network == network)
        query = query.group_by(WaveformChannel.station)
        data = formatORMResults(request, query)
        session.close()
        return data


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
        if network:
            query = query.filter(WaveformChannel.network == network)
        if station:
            query = query.filter(WaveformChannel.station == station)
        query = query.group_by(WaveformChannel.location)
        data = formatORMResults(request, query)
        session.close()
        return data



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
        if network:
            query = query.filter(WaveformChannel.network == network)
        if station:
            query = query.filter(WaveformChannel.station == station)
        if location:
            query = query.filter(WaveformChannel.location == location)
        query = query.group_by(WaveformChannel.channel)
        data = formatORMResults(request, query)
        session.close()
        return data


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
        data = formatORMResults(request, query)
        session.close()
        return data


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
        session.close()
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
                              WaveformChannel.channel,
                              WaveformFile.format)
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
        apply_filter = request.args0.get('apply_filter', None)
        # execute query
        results = query.all()
        session.close()
        # check for results
        stream = Stream()
        if len(results) == 0:
            # ok lets use arclink
            try:
                stream = self._fetchFromArclink(request, start, end)
            except:
                pass
        else:
            # get from local waveform archive
            for result in results:
                fname = result[0] + os.sep + result[1]
                try:
                    st = read(fname, format=result[6], starttime=start,
                              endtime=end)
                except ChksumError:
                    try:
                        st = read(fname, format=result[6], starttime=start,
                                  endtime=end, verify_chksum=False)
                    except:
                        continue
                except:
                    continue
                # trim
                st.trim(start, end)
                for tr in st:
                    if apply_filter is not None:
                        tr.stats.network = result[2]
                        tr.stats.station = result[3]
                        tr.stats.location = result[4]
                        tr.stats.channel = result[5]
                    stream.append(tr)
                del st
        # pickle stream
        data = pickle.dumps(stream, protocol=2)
        del stream
        # generate correct header
        request.setHeader('content-type', 'binary/octet-stream')
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
        # cut
        st.trim(start, end)
        # write to arclink directory
        rpath = os.path.join(self.env.getInstancePath(), 'data', 'arclink')
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
        return st

    def _checkPath(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)


class WaveformPreviewMapper(Component):
    """
    Returns a requested waveform preview.
    """
    implements(IMapper)

    mapping_url = '/seismology/waveform/getPreview'

    def process_GET(self, request):
        # get format
        formats = request.args.get('format', []) or \
            request.args.get('output', [])
        if 'json' in formats:
            return self._createJSON(request)
        elif 'png' in formats or 'image' in formats:
            return self._createImage(request)
        else:
            return self._createPickle(request)

    def _createPickle(self, request):
        st, _, _ = _getPreview(self.env.db.session(), **request.args0)
        # pickle
        data = pickle.dumps(st, protocol=2)
        # generate correct header
        request.setHeader('content-type', 'binary/octet-stream')
        return data

    def _createImage(self, request):
        st, start, end = _getPreview(self.env.db.session(), **request.args0)
        st.trim(start, end, pad=True)
        # create a full stream object
        for tr in st:
            tr.data[tr.data == -1] = np.ma.masked
            muh = np.empty(len(tr.data) * 2, tr.data.dtype)
            muh[0::2] = tr.data
            muh[1::2] = -tr.data
            tr.data = muh
            tr.stats.delta = tr.stats.delta / 2
        # XXX
        st.sort()
        try:
            data = st.plot(format="png")
        except:
            return ''
        # set content type
        request.setHeader('content-type', 'image/png')
        return data

    def _createJSON(self, request):
        st, start, end = _getPreview(self.env.db.session(), **request.args0)
        st.trim(start, end, pad=True)
        # build up JSON string
        data = {}
        for tr in st:
            data[tr.id] = {}
            data[tr.id]['stats'] = dict(tr.stats)
            data[tr.id]['data'] = tr.data.tolist()
        # set content type
        request.setHeader('content-type', 'application/json; charset=UTF-8')
        return json.dumps({'stream': data}, cls=CustomJSONEncoder, indent=4)
