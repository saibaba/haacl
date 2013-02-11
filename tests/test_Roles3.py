import dsl
from dsl import *
import unittest

class Roles3(unittest.TestCase):

    def setUp(self):
        self.request_context =  {
            'method' : 'GET',
            'url' : '/lblist/chargeable?startTime=2010-12-15&endTime=2011-5-1&offset=2&limit=2',
            'subject' : {
                'role' : 'Create',
            },
        }
        dsl.dsl_debug = False

    def test_rule1(self):


        # Rule 1: Allow GET on /lblist/chargeable?startTime=2010-12-15&endTime=2011-5-1&offset=2&limit=2 for subject with role Create or Update or Delete or Read/Only

        rule = (Method == Http.GET) \
            & (Url / ".*/lblist/chargeable\?startTime=2010-12-15&endTime=2011-5-1&offset=2&limit=2") \
            & ( Subject.role.In(['Create', 'Update', 'Delete', 'Read/Only']) )

        self.assertTrue(rule.eval(self.request_context, {}))

        self.request_context['url'] = "http://www.service.com/ctx/path/servers/devices/1"
        self.assertFalse(rule.eval(self.request_context, {}))

