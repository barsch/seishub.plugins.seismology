# -*- coding: utf-8 -*-
"""
"""

from lxml.etree import Element, SubElement as Sub
from seishub.core import Component, implements
from seishub.packages.interfaces import IAdminPanel, IMapper
from seishub.util.xmlwrapper import toString
from sqlalchemy import sql
import os


class StationsPanel(Component):
    """
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
        if nid == '*':
            nid = False
            sid = False
        elif sid == '*' or nid_changed:
            sid = False
        # set data
        data = {}
        data['network_id'] = nid or ''
        data['station_id'] = sid or ''
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


class StationsMapper(Component):
    """
    """
    implements(IMapper)

    package_id = 'seismology'
    mapping_url = '/seismology/station/getStationList'

    def process_GET(self, request):
        # parse input arguments
        network_id = request.args0.get('network_id', '')
        station_id = request.args0.get('station_id', '')
        status = request.args0.get('status', '')
        all = request.args0.get('all', False)
        try:
            offset = int(request.args0.get('offset', 0))
            limit = int(request.args0.get('limit', 20))
        except:
            offset = 0
            limit = None
        # filter indexes
        catalog = self.env.catalog.index_catalog
        xmlindex_list = catalog.getIndexes('seismology', 'station')[::-1]
        if not all:
            filter = ['latitude', 'longitude', 'start_datetime',
                      'end_datetime', 'station_id', 'network_id',
                      'station_name', 'elevation']
            xmlindex_list = [x for x in xmlindex_list if x.label in filter]
        if not xmlindex_list:
            return
        # build up query
        query, joins = catalog._createIndexView(xmlindex_list, compact=False)
        query = query.select_from(joins)
        if network_id != '':
            query = query.where(
                sql.literal_column('network_id.keyval') == network_id)
        if station_id != '':
            query = query.where(
                sql.literal_column('station_id.keyval') == station_id)
        if status == 'active':
            query = query.where(
                sql.literal_column('end_datetime.keyval') == None)
        elif status == 'inactive':
            query = query.where(
                sql.literal_column('end_datetime.keyval') != None)

        # count all possible results
        try:
            results = self.env.db.query(query).fetchall()
            count = len(results)
        except:
            count = 0
        # generate XML result
        xml = Element("query", total_results=str(count))
        # execute query
        query = query.order_by(sql.literal_column('network_id.keyval'))
        query = query.order_by(sql.literal_column('station_id.keyval'))
        if all:
            query = query.order_by(sql.literal_column('location_id.keyval'))
            query = query.order_by(sql.literal_column('channel_id.keyval'))
        query = query.order_by(sql.literal_column('start_datetime.keyval'))
        query = query.offset(offset).limit(limit)
        if limit:
            query = query.limit(limit)
        try:
            results = self.env.db.query(query).fetchall()
            if not results:
                return toString(xml)
        except:
            return toString(xml)
        # cycle over results
        xml.attrib['results_returned'] = str(len(results))
        for result in results:
            s = Sub(xml, "resource")
            for (key, value) in dict(result).iteritems():
                if value == None:
                    value = ''
                Sub(s, key).text = str(value)
        return toString(xml)
