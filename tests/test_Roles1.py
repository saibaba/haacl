import dsl
from dsl import *
import unittest

class Roles1(unittest.TestCase):

    def setUp(self):
        self.request_context =  {
            'method' : 'GET',
            'url' : 'http://www.service.com/ctx/path/servers/1',
            'subject' : { 
                'role' : 'Create',
            },
        }
        dsl.dsl_debug = False

    def test_rule1(self):


        # Rule 1: Allow GET on /servers/{serverID} for subject with role Create or Update or Delete or Read/Only

        rule = (Method == GET) \
            & (Url / ".*/servers/[^/]+$") \
            & ( Subject.role.In(['Create', 'Update', 'Delete', 'Read/Only']) )

        self.assertTrue(rule.eval(self.request_context, {}))

        self.request_context['url'] = "http://www.service.com/ctx/path/servers/devices/1"
        self.assertFalse(rule.eval(self.request_context, {}))

    def test_rule2(self):


        # Rule 2: Allow DELETE on /servers/{serverID} for subject with role Delete

        rule = (Method == Http.DELETE) \
            & (Url / ".*/servers/[^/]+$") \
            & ( Subject.role.In(['Delete']) )

        self.request_context['method'] = 'DELETE'
        self.request_context['subject']['role'] = 'Delete'
        self.assertTrue(rule.eval(self.request_context, {}))

        self.request_context['method'] = 'POST'
        self.assertFalse(rule.eval(self.request_context, {}))

        self.request_context['url'] = "http://www.service.com/ctx/path/servers/devices/1"
        self.assertFalse(rule.eval(self.request_context, {}))

