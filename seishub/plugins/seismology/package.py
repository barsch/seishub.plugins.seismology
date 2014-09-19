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
    '/{http://quakeml.org/xmlns/quakeml/1.2}quakeml/eventParameters/event[position()=1]'
XPATH_ORIGIN_PREFERRED = (
    '%s/origin[@publicID=string(../preferredOriginID/text())]'
    % XPATH_EVENT)
XPATH_ORIGIN_FIRST = '%s/origin[position()=1]' % XPATH_EVENT
XPATH_MAGNITUDE_PREFERRED = (
    '%s/magnitude[@publicID=string(../preferredMagnitudeID/text())]'
    % XPATH_EVENT)
XPATH_MAGNITUDE_FIRST = '%s/magnitude[position()=1]' % XPATH_EVENT
XPATH_FOCALMECHANISM_PREFERRED = (
    '%s/focalMechanism[@publicID=string(../preferredFocalMechanismID/text())]'
    % XPATH_EVENT)
XPATH_FOCALMECHANISM_FIRST = '%s/focalMechanism[position()=1]' % XPATH_EVENT
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
    registerStylesheet('xslt' + os.sep + 'seiscomp2quakeml.xslt', 'seiscomp')

    registerIndex('event_type', '%s/type' % XPATH_EVENT, 'text')
    registerIndex('evaluation_mode',
                  '%s/{%s}evaluationMode' % (XPATH_EVENT, NAMESPACE_EDB),
                  'text')
    registerIndex('author', '%s/creationInfo/author' % XPATH_EVENT, 'text')
    registerIndex('public',
                  '%s/{%s}public' % (XPATH_EVENT, NAMESPACE_EDB),
                  'boolean')

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


class DatetimeIndex(Component):
    """
    Indexes origin time of an event resource.
    Looks up preferred origin or if it is not defined uses the first origin
    in the document.
    """
    implements(IProcessorIndex)

    package_id = 'seismology'
    resourcetype_id = 'event'
    type = index.DATETIME_INDEX
    type_mapper = UTCDateTime
    label = 'datetime'
    xpath_head1 = XPATH_ORIGIN_PREFERRED
    xpath_head2 = XPATH_ORIGIN_FIRST
    xpath_tail = "/time/value"

    def eval(self, document):
        doc = document.getXml_doc()
        values = doc.evalXPath('%s%s' % (self.xpath_head1, self.xpath_tail))
        print "-" * 30
        print [str(v) for v in values]
        if values:
            return self.type_mapper(str(values[0]))
        values = doc.evalXPath('%s%s' % (self.xpath_head2, self.xpath_tail))
        print [str(v) for v in values]
        if values:
            return self.type_mapper(str(values[0]))
        return None


class LatitudeIndex(DatetimeIndex):
    type = index.NUMERIC_INDEX
    type_mapper = float
    label = 'latitude'
    xpath_tail = "/latitude/value"


class LongitudeIndex(LatitudeIndex):
    label = 'longitude'
    xpath_tail = "/longitude/value"


class DepthIndex(LatitudeIndex):
    label = 'depth'
    xpath_tail = "/depth/value"


class PhaseCountIndex(LatitudeIndex):
    type = index.INTEGER_INDEX
    type_mapper = int
    label = 'used_phase_count'
    xpath_tail = "/quality/usedPhaseCount"


class PhaseCountPIndex(PhaseCountIndex):
    label = 'used_phase_count_p'
    xpath_tail = '/quality/{%s}usedPhaseCountP' % NAMESPACE_EDB


class PhaseCountSIndex(PhaseCountIndex):
    label = 'used_phase_count_s'
    xpath_tail = '/quality/{%s}usedPhaseCountS' % NAMESPACE_EDB


class MagnitudeIndex(LatitudeIndex):
    label = 'magnitude'
    xpath_head1 = XPATH_MAGNITUDE_PREFERRED
    xpath_head2 = XPATH_MAGNITUDE_FIRST
    xpath_tail = "/mag/value"


class MagnitudeTypeIndex(MagnitudeIndex):
    type = index.TEXT_INDEX
    type_mapper = str
    label = 'magnitude_type'
    xpath_tail = "/type"


class Np1StrikeIndex(LatitudeIndex):
    label = 'np1_strike'
    xpath_head1 = XPATH_FOCALMECHANISM_PREFERRED
    xpath_head2 = XPATH_FOCALMECHANISM_FIRST
    xpath_tail = "/nodalPlanes/nodalPlane1/strike/value"


class Np1DipIndex(Np1StrikeIndex):
    label = 'np1_dip'
    xpath_tail = "/nodalPlanes/nodalPlane1/dip/value"


class Np1RakeIndex(Np1StrikeIndex):
    label = 'np1_rake'
    xpath_tail = "/nodalPlanes/nodalPlane1/rake/value"


class MRRIndex(Np1StrikeIndex):
    label = 'mt_mrr'
    xpath_tail = "/momentTensor/tensor/Mrr/value"


class MTTIndex(Np1StrikeIndex):
    label = 'mt_mtt'
    xpath_tail = "/momentTensor/tensor/Mtt/value"


class MPPIndex(Np1StrikeIndex):
    label = 'mt_mpp'
    xpath_tail = "/momentTensor/tensor/Mpp/value"


class MRTIndex(Np1StrikeIndex):
    label = 'mt_mrt'
    xpath_tail = "/momentTensor/tensor/Mrt/value"


class MRPIndex(Np1StrikeIndex):
    label = 'mt_mrp'
    xpath_tail = "/momentTensor/tensor/Mrp/value"


class MTPIndex(Np1StrikeIndex):
    label = 'mt_mtp'
    xpath_tail = "/momentTensor/tensor/Mtp/value"
