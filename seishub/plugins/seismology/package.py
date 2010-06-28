# -*- coding: utf-8 -*-
"""
Seismology package for SeisHub.
"""

from seishub.core import Component, implements
from seishub.packages.installer import registerIndex, registerSchema, \
    registerStylesheet, registerAlias
from seishub.packages.interfaces import IProcessorIndex, IPackage, \
    IResourceType
from seishub.xmldb import index
import os
from obspy.core import UTCDateTime


class SeismologyPackage(Component):
    """
    Seismology package for SeisHub.
    """
    implements(IPackage)

    package_id = 'seismology'
    version = '0.1'


class SeismicStationResourceType(Component):
    """
    A station resource type for package seismology.
    """
    implements(IResourceType)

    package_id = 'seismology'
    resourcetype_id = 'station'

    registerSchema('xsd' + os.sep + 'xml-seed-1.1.xsd', 'XMLSchema')
    registerStylesheet('xslt' + os.sep + 'station_googlemaps_xhtml.xslt',
                       'map')
    registerStylesheet('xslt' + os.sep + 'station_metadata.xslt', 'metadata')

    registerIndex('network_id',
                  '/xseed/station_control_header#' + \
                  'station_identifier/network_code',
                  'text')
    registerIndex('station_id',
                  '/xseed/station_control_header#' + \
                  'station_identifier/station_call_letters',
                  'text')
    registerIndex('location_id',
                  '/xseed/station_control_header/channel_identifier#' + \
                  'location_identifier',
                  'text')
    registerIndex('channel_id',
                  '/xseed/station_control_header/channel_identifier#' + \
                  'channel_identifier',
                  'text')
    registerIndex('station_name',
                  '/xseed/station_control_header#station_identifier/site_name',
                  'text')
    registerIndex('latitude',
                  '/xseed/station_control_header#station_identifier/latitude',
                  'float')
    registerIndex('longitude',
                  '/xseed/station_control_header#station_identifier/longitude',
                  'float')
    registerIndex('elevation',
                  '/xseed/station_control_header#station_identifier/elevation',
                  'float')
    registerIndex('start_datetime',
                  '/xseed/station_control_header#' + \
                  'station_identifier/start_effective_date',
                  'datetime')
    registerIndex('end_datetime',
                  '/xseed/station_control_header#' + \
                  'station_identifier/end_effective_date',
                  'datetime')
    registerIndex('quality',
                  '/xseed/station_control_header#' + \
                  'station_identifier/quality',
                  'numeric')


class SeismicEventResourceType(Component):
    """
    A event resource type for package seismology.
    """
    implements(IResourceType)

    package_id = 'seismology'
    resourcetype_id = 'event'

    registerStylesheet('xslt' + os.sep + 'event_metadata.xslt', 'metadata')
    registerStylesheet('xslt' + os.sep + 'event_googlemaps_xhtml.xslt', 'map')
    registerStylesheet('xslt' + os.sep + 'seiscomp2earthworm.xslt', 'seiscomp')

    registerIndex('datetime',
                  '/event/origin/time/value',
                  'datetime')
    registerIndex('latitude',
                  '/event/origin/latitude/value',
                  'numeric')
    registerIndex('longitude',
                  '/event/origin/longitude/value',
                  'numeric')
    registerIndex('depth',
                  '/event/origin/depth/value',
                  'numeric')
    registerIndex('used_p',
                  '/event/origin/originQuality/P_usedPhaseCount',
                  'integer')
    registerIndex('used_s',
                  '/event/origin/originQuality/S_usedPhaseCount',
                  'integer')
    registerIndex('magnitude',
                  '/event/magnitude/mag/value',
                  'numeric')
    registerIndex('magnitude_type',
                  '/event/magnitude/type',
                  'text')
    registerIndex('np1_strike',
                  '/event/focalMechanism/nodalPlanes/nodalPlane1/strike/value',
                  'numeric')
    registerIndex('np1_dip',
                  '/event/focalMechanism/nodalPlanes/nodalPlane1/dip/value',
                  'numeric')
    registerIndex('np1_rake',
                  '/event/focalMechanism/nodalPlanes/nodalPlane1/rake/value',
                  'numeric')
    registerIndex('mt_mrr',
                  '/event/focalMechanism/momentTensor/tensor/Mrr/value',
                  'numeric')
    registerIndex('mt_mtt',
                  '/event/focalMechanism/momentTensor/tensor/Mtt/value',
                  'numeric')
    registerIndex('mt_mpp',
                  '/event/focalMechanism/momentTensor/tensor/Mpp/value',
                  'numeric')
    registerIndex('mt_mrt',
                  '/event/focalMechanism/momentTensor/tensor/Mrt/value',
                  'numeric')
    registerIndex('mt_mrp',
                  '/event/focalMechanism/momentTensor/tensor/Mrp/value',
                  'numeric')
    registerIndex('mt_mtp',
                  '/event/focalMechanism/momentTensor/tensor/Mtp/value',
                  'numeric')
    registerIndex('event_type', '/event/type', 'text')
    registerIndex('localisation_method', '/event/event_type/value', 'text')
    registerIndex('user', '/event/event_type/user', 'text')
    registerIndex('account', '/event/event_type/account', 'text')
    registerIndex('public', '/event/event_type/public', 'boolean')

    registerAlias('/seismology/event/last20BigEvents',
                  "/seismology/event[magnitude>=2.0] " + \
                  "ORDER BY datetime ASC LIMIT 20")


class FirstPickIndex(Component):
    """
    Indexes the date and time of the first pick of an event resource.
    """
    implements(IProcessorIndex)

    package_id = 'seismology'
    resourcetype_id = 'event'
    type = index.DATETIME_INDEX
    label = 'first_pick'

    def eval(self, document):
        # fetch all pick times
        doc = document.getXml_doc()
        picks = doc.evalXPath('/event/pick/time/value/text()')
        if not picks:
            return None
        # get first pick
        saved = UTCDateTime(str(picks[0]))
        for pick in picks[1:]:
            temp = UTCDateTime(str(pick))
            if temp < saved:
                saved = temp
        return saved


class LastPickIndex(Component):
    """
    Indexes the date and time of the last pick of an event resource.
    """
    implements(IProcessorIndex)

    package_id = 'seismology'
    resourcetype_id = 'event'
    type = index.DATETIME_INDEX
    label = 'last_pick'

    def eval(self, document):
        # fetch all pick times
        doc = document.getXml_doc()
        picks = doc.evalXPath('/event/pick/time/value/text()')
        if not picks:
            return None
        # get last pick
        saved = UTCDateTime(str(picks[0]))
        for pick in picks[1:]:
            temp = UTCDateTime(str(pick))
            if temp > saved:
                saved = temp
        return saved
