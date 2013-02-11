from dsl import *
import unittest
import dsl

class HttpHeaderTests(unittest.TestCase):

    def setUp(self):
        self.request_context =  {
            'method' : 'GET',
            'url' : '/loadbalancers/billable?startTime=2010-12-15&endTime=2011-5-1&offset=2&limit=2',
            'headers' : { "Content-Type" : "application/json" , 'X-Tenant-Id' : 'tenant1'}, 
            'subject' : {
                'role' : 'Create',
            },
        }
        dsl.dsl_debug = False

    def test_rule1(self):


        # Rule 1: 

        rule = (Method == Http.GET) \
            & (Headers["Content-Type"] == "application/json") \
            & ( Subject.role.In(['Create', 'Update', 'Delete', 'Read/Only']) )

        self.assertTrue(rule.eval(self.request_context, {}))
        self.request_context['headers']['Content-Type'] = "application/xml"
        self.assertFalse(rule.eval(self.request_context, {}))

    def test_rule2(self):

        # Rule 2: Allow GET on /tenants/{tenantId}/servers/{serverId} if the http header "X-Tenant-Id" matches tenantId

        rule = (Method == GET) \
               & (Url % '/tenants/{tenantId}/servers/{serverId}') \
               & (Url['tenantId'] == Headers['X-Tenant-Id'])

        self.request_context['url'] = '/tenants/T12345/servers/Scfx-123-1221-cfg-92a'
        self.assertFalse(rule.eval(self.request_context, {}))

        self.request_context['headers']['X-Tenant-Id'] = "T12345"
        self.assertTrue(rule.eval(self.request_context, {}))
