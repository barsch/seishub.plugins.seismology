# -*- coding: utf-8 -*-
"""
Seismology package for SeisHub.
"""

from StringIO import StringIO
from obspy.core import UTCDateTime
from obspy.xseed import Parser
from seishub.core import Component, implements
from seishub.db.util import formatResults
from seishub.packages.interfaces import IMapper, IResourceFormater, IAdminPanel
from sqlalchemy import sql, Table
import os
import zipfile


class DatalessFormater(Component):
    """
    Dataless representation of a seismic station resource.
    """
    implements(IResourceFormater)

    package_id = "seismology"
    resourcetype_id = "station"
    format_id = ["dataless", "seed"]

    @staticmethod
    def format(request, data, res_name):
        """
        """
        try:
            p = Parser()
            p.read(data)
            result = p.getSEED()
        except:
            return data
        # set file name
        request.setHeader('Content-Disposition',
                          'attachment; filename=%s.dataless' \
                          % res_name)
        # set content type
        request.setHeader('content-type',
                          'application/octet-stream')
        return result


class RESPFormater(Component):
    """
    RESP representation of a seismic station resource.
    """
    implements(IResourceFormater)

    package_id = "seismology"
    resourcetype_id = "station"
    format_id = ["resp", "response"]

    @staticmethod
    def format(request, data, res_name):
        """
        """
        channel = str(request.args0.get('channel', '')).upper()
        try:
            p = Parser()
            p.read(data)
            resp_list = p.getRESP()
            # Create a ZIP archive.
            zip_fh = StringIO()
            if channel == '':
                zip_file = zipfile.ZipFile(zip_fh, "w")
                for response in resp_list:
                    response[1].seek(0, 0)
                    zip_file.writestr(response[0], response[1].read())
                zip_file.close()
                zip_fh.seek(0)
                data = zip_fh.read()
                res_name += os.extsep + "zip"
            else:
                for response in resp_list:
                    if response[0][-3:] != channel:
                        continue
                    response[1].seek(0, 0)
                    data = response[1].read()
                    res_name = response[0]
                    break
        except:
            return data
        if channel == '':
            # set content type
            request.setHeader('content-type', 'application/zip')
        # set file name
        request.setHeader('Content-Disposition',
                         'attachment; filename=%s' % res_name)
        return data


class StationPanel(Component):
    """
    A seismic station overview for the administrative web interface.
    """
    implements(IAdminPanel)

    template = 'templates' + os.sep + 'stations.tmpl'
    panel_ids = ('seismology', 'Seismology', 'stations', 'Stations')

    def render(self, request):
        # fetch args
        nid = request.args0.get('network_id', False)
        nid_changed = request.args0.get('network_id_button', False)
        sid = request.args0.get('station_id', False)
        status = request.args0.get('status', '')
        # reset + defaults
        if nid == '*' or nid_changed:
            sid = '*'
        # set data
        data = {}
        data['network_id'] = nid or '*'
        data['station_id'] = sid or '*'
        data['status'] = status or ''
        data['network_ids'] = self._getNetworkIDs()
        data['station_ids'] = self._getStationIDs(nid)
        return data

    def _getNetworkIDs(self):
        """
        Fetches all possible network id's.
        """
        # network
        query = sql.text("""
            SELECT DISTINCT(network_id) 
            FROM "/seismology/station"
            ORDER BY network_id
        """)
        # execute query
        try:
            results = self.env.db.query(query)
            result = [r[0] for r in results]
        except:
            result = []
        return result

    def _getStationIDs(self, network_id=False):
        """
        Fetches all station id's of given network id.
        """
        if not network_id:
            return []
        query = sql.text("""
            SELECT DISTINCT(station_id) 
            FROM "/seismology/station"
            WHERE network_id = :network_id
            ORDER BY station_id
        """)
        # execute query
        try:
            results = self.env.db.query(query, network_id=network_id)
            result = [r[0] for r in results]
        except:
            result = []
        return result


class StationListMapper(Component):
    """
    Generates a list of available seismic stations.
    """
    implements(IMapper)

    package_id = 'seismology'
    mapping_url = '/seismology/station/getList'

    def process_GET(self, request):
        """
        """
        # parse input arguments
        tab = Table('/seismology/station', request.env.db.metadata,
                    autoload=True)
        # fetch arguments
        try:
            limit = int(request.args0.get('limit'))
        except:
            limit = None
        offset = int(request.args0.get('offset', 0))
        # build up query
        columns = [tab.c['document_id'], tab.c['package_id'],
                   tab.c['resourcetype_id'], tab.c['resource_name'],
                   tab.c['network_id'], tab.c['station_id'],
                   tab.c['station_name'], tab.c['latitude'],
                   tab.c['longitude'], tab.c['elevation'], tab.c['quality'],
                   tab.c['start_datetime'], tab.c['end_datetime']]
        query = sql.select(columns, distinct=True,
                           order_by=[tab.c['network_id'],
                                     tab.c['station_id'],
                                     tab.c['start_datetime']])
        # process arguments
        # datetime
        try:
            datetime = UTCDateTime(request.args0.get('datetime')).datetime
            query = query.where(tab.c['start_datetime'] <= datetime)
            query = query.where(sql.or_(tab.c['end_datetime'] >= datetime,
                                        tab.c['end_datetime'] == None))
        except:
            pass
        # status
        try:
            status = request.args0.get('status')
            if status == 'active':
                query = query.where(tab.c['end_datetime'] == None)
            elif status == 'inactive':
                query = query.where(tab.c['end_datetime'] != None)
        except:
            pass
        # network, station, location. channel
        for col in ['network_id', 'station_id', 'location_id', 'channel_id']:
            text = request.args0.get(col, None)
            if text is None:
                continue
            elif text == '':
                query = query.where(tab.c[col] == None)
            elif '*' in text or '?' in text:
                text = text.replace('?', '_')
                text = text.replace('*', '%')
                query = query.where(tab.c[col].like(text))
            else:
                query = query.where(tab.c[col] == text)
        # execute query
        try:
            results = request.env.db.query(query.offset(offset).limit(limit))
        except:
            results = []
        try:
            count = len([1 for _i in request.env.db.query(query)])
        except:
            count = 0
        return formatResults(request, results, limit=limit, offset=offset,
                             count=count, build_url=True)
