# -*- coding: utf-8 -*-
"""
A test suite for station resources.
"""

from StringIO import StringIO
from obspy.xseed import Parser
from seishub.core.processor import PUT, DELETE, Processor
from seishub.core.processor.processor import GET
from seishub.core.test import SeisHubEnvironmentTestCase
from seishub.plugins.seismology import package, station
import glob
import os
import unittest


class StationTests(SeisHubEnvironmentTestCase):
    """
    A test suite for station resources.
    """
    def setUp(self):
        self.env.enableComponent(package.SeismologyPackage)
        self.env.enableComponent(package.SeismicStationResourceType)
        self.env.enableComponent(station.StationListMapper)
        self.env.tree.update()

    def tearDown(self):
        self.env.registry.schemas.deleteAll('seismology', 'station')
        # XXX: this should be self.env.registry.indexes.delete
        self.env.catalog.deleteAllIndexes('seismology', 'station')
        self.env.registry.stylesheets.deleteAll('seismology', 'station')
        self.env.registry.db_deleteResourceType('seismology', 'station')
        self.env.registry.db_deletePackage('seismology')

    def test_stationResource(self):
        """
        Test creating, reading and deleting of station resources.
        """
        proc = Processor(self.env)
        path = os.path.dirname(__file__)
        dataless_file = os.path.join(path, 'data', 'dataless-odc.BW_MANZ')
        data = Parser(dataless_file).getXSEED()
        # POST a resource
        proc.run(PUT, '/xml/seismology/station/BW_MANZ.xml', StringIO(data))
        # check if resource exists and compare results
        res = proc.run(GET, '/xml/seismology/station/BW_MANZ.xml')
        data2 = res.render(proc)
        self.assertTrue(data2.startswith('<?xml'))
        self.assertTrue('BW - BAYERNNETZ, GERMANY' in data2)
        # delete resource
        proc.run(DELETE, '/xml/seismology/station/BW_MANZ.xml')

    def test_getListMapper(self):
        """
        Tests StationListMapper.
        """
        proc = Processor(self.env)
        # add some test resources
        path = os.path.dirname(__file__)
        files = glob.glob(os.path.join(path, 'data', 'dataless-odc.*'))
        for dataless_file in files:
            filename = os.path.basename(dataless_file).split('.')[1]
            data = Parser(dataless_file).getXSEED()
            proc.run(PUT, '/xml/seismology/station/%s.xml' % (filename),
                     StringIO(data))
        # check if resource exists
        res = proc.run(GET, '/xml/seismology/station/BW_MANZ.xml')
        data2 = res.render(proc)
        self.assertTrue(data2.startswith('<?xml'))
        self.assertTrue('BW - BAYERNNETZ, GERMANY' in data2)
        # enable and query mapper
        res = proc.run(GET, '/seismology/station/getList')
        self.assertTrue('<package_id>seismology</package_id>' in res)
        self.assertTrue('<resourcetype_id>station</resourcetype_id>' in res)
        self.assertTrue('<network_id>BW</network_id>' in res)
        self.assertTrue('<station_id>MANZ</station_id>' in res)
        # delete all resources
        files = glob.glob(os.path.join(path, 'data', 'dataless-odc.*'))
        for dataless_file in files:
            filename = os.path.basename(dataless_file).split('.')[1]
            proc.run(DELETE, '/xml/seismology/station/%s.xml' % (filename))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StationTests, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
