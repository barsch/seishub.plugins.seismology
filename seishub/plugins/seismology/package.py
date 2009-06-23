# -*- coding: utf-8 -*-
"""
Seismology package for SeisHub.
"""

from seishub.core import Component, implements
from seishub.packages.installer import registerIndex, registerSchema, \
    registerStylesheet
from seishub.packages.interfaces import IAdminPanel, IPackage, IResourceType
import os


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

    registerSchema('xsd' + os.sep + 'xml-seed.modified.xsd', 'XMLSchema')
    registerStylesheet('xslt' + os.sep + 'station_googlemaps_xhtml.xslt', 'map')
    registerStylesheet('xslt' + os.sep + 'station_metadata.xslt', 'metadata')

    registerIndex('network_id',
                  '/xseed/station_control_header#station_identifier/network_code',
                  'text')
    registerIndex('station_id',
                  '/xseed/station_control_header#station_identifier/station_call_letters',
                  'text')
    registerIndex('location_id',
                  '/xseed/station_control_header/channel_identifier#location_identifier',
                  'text')
    registerIndex('channel_id',
                  '/xseed/station_control_header/channel_identifier#channel_identifier',
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
                  '/xseed/station_control_header#station_identifier/start_effective_date',
                  'datetime')
    registerIndex('end_datetime',
                  '/xseed/station_control_header#station_identifier/end_effective_date',
                  'datetime')


class SeismicEventResourceType(Component):
    """
    A event resource type for package seismology.
    """
    implements(IResourceType)

    package_id = 'seismology'
    resourcetype_id = 'event'

    registerStylesheet('xslt' + os.sep + 'event_metadata.xslt', 'metadata')
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
    registerIndex('localisation_method', '/event/event_type', 'text')


class WaveformsPanel(Component):
    """
    """
    implements(IAdminPanel)

    template = 'templates' + os.sep + 'waveforms.tmpl'
    panel_ids = ('seismology', 'Seismology', 'waveforms', 'Waveforms')

    def render(self, request):
        data = {}
        data['current_seed_files'] = len(self.env.current_seed_files)
        return data


class EventsPanel(Component):
    """
    """
    implements(IAdminPanel)

    template = 'templates' + os.sep + 'events.tmpl'
    panel_ids = ('seismology', 'Seismology', 'events', 'Events')

    def render(self, request):
        data = {}
        return data


