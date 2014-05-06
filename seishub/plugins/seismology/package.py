# -*- coding: utf-8 -*-
"""
Seismology package for SeisHub.
"""

from obspy.core import UTCDateTime
from obspy.db.db import Base
from seishub.core.core import Component, implements
from seishub.core.packages.installer import registerIndex, registerSchema, \
    registerStylesheet, registerAlias
from seishub.core.packages.interfaces import IProcessorIndex, IPackage, \
    IResourceType
from seishub.core.xmldb import index
import os


XPATH_EVENT = \
    '/{http://quakeml.org/xmlns/quakeml/1.2}quakeml/eventParameters/event'
NAMESPACE_EDB = "http://erdbeben-in-bayern.de/xmlns/0.1"


class SeismologyPackage(Component):
    """
    Seismology package for SeisHub.
    """
    implements(IPackage)

    package_id = 'seismology'
    version = '0.1'

    def __init__(self, *args, **kwargs):
        super(SeismologyPackage, self).__init__(*args, **kwargs)
        # initialize obspy.db tables
        Base.metadata.create_all(self.env.db.engine, checkfirst=True)


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

    registerSchema('relaxng' + os.sep + 'QuakeML-1.2-merged.rng', 'RelaxNG')
    registerStylesheet('xslt' + os.sep + 'event_metadata.xslt', 'metadata')
    registerStylesheet('xslt' + os.sep + 'event_googlemaps_xhtml.xslt', 'map')
    registerStylesheet('xslt' + os.sep + 'seiscomp2earthworm.xslt', 'seiscomp')

    registerIndex('datetime',
                  '%s/origin/time/value' % XPATH_EVENT,
                  'datetime')
    registerIndex('latitude',
                  '%s/origin/latitude/value' % XPATH_EVENT,
                  'numeric')
    registerIndex('longitude',
                  '%s/origin/longitude/value' % XPATH_EVENT,
                  'numeric')
    registerIndex('depth',
                  '%s/origin/depth/value' % XPATH_EVENT,
                  'numeric')
    registerIndex('used_phase_count',
                  '%s/origin/quality/usedPhaseCount' % XPATH_EVENT,
                  'integer')
    registerIndex('used_phase_count_p',
                  '%s/origin/quality/usedPhaseCountP' % XPATH_EVENT,
                  'integer')
    registerIndex('used_phase_count_s',
                  '%s/origin/quality/usedPhaseCountS' % XPATH_EVENT,
                  'integer')
    registerIndex('magnitude',
                  '%s/magnitude/mag/value' % XPATH_EVENT,
                  'numeric')
    registerIndex('magnitude_type',
                  '%s/magnitude/type' % XPATH_EVENT,
                  'text')
    registerIndex('np1_strike',
                  '%s/focalMechanism/nodalPlanes/nodalPlane1/strike/value' % XPATH_EVENT,
                  'numeric')
    registerIndex('np1_dip',
                  '%s/focalMechanism/nodalPlanes/nodalPlane1/dip/value' % XPATH_EVENT,
                  'numeric')
    registerIndex('np1_rake',
                  '%s/focalMechanism/nodalPlanes/nodalPlane1/rake/value' % XPATH_EVENT,
                  'numeric')
    registerIndex('mt_mrr',
                  '%s/focalMechanism/momentTensor/tensor/Mrr/value' % XPATH_EVENT,
                  'numeric')
    registerIndex('mt_mtt',
                  '%s/focalMechanism/momentTensor/tensor/Mtt/value' % XPATH_EVENT,
                  'numeric')
    registerIndex('mt_mpp',
                  '%s/focalMechanism/momentTensor/tensor/Mpp/value' % XPATH_EVENT,
                  'numeric')
    registerIndex('mt_mrt',
                  '%s/focalMechanism/momentTensor/tensor/Mrt/value' % XPATH_EVENT,
                  'numeric')
    registerIndex('mt_mrp',
                  '%s/focalMechanism/momentTensor/tensor/Mrp/value' % XPATH_EVENT,
                  'numeric')
    registerIndex('mt_mtp',
                  '%s/focalMechanism/momentTensor/tensor/Mtp/value' % XPATH_EVENT,
                  'numeric')
    registerIndex('event_type', '%s/type' % XPATH_EVENT, 'text')
    registerIndex('evaluation_mode', '%s/{%s}evaluationMode' % (XPATH_EVENT, NAMESPACE_EDB), 'text')
    registerIndex('author', '%s/creationInfo/author' % XPATH_EVENT, 'text')
    registerIndex('public', '%s/{%s}public' % (XPATH_EVENT, NAMESPACE_EDB), 'boolean')

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
        picks = doc.evalXPath('%s/pick/time/value' % XPATH_EVENT)
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
        picks = doc.evalXPath('%s/pick/time/value' % XPATH_EVENT)
        if not picks:
            return None
        # get last pick
        saved = UTCDateTime(str(picks[0]))
        for pick in picks[1:]:
            temp = UTCDateTime(str(pick))
            if temp > saved:
                saved = temp
        return saved
