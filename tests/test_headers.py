import dsl
from dsl import *
import unittest

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
        dsl.debug = True

    def test_rule1(self):


        # Rule 1: Allow GET on /loadbalancers/billable?startTime=2010-12-15&endTime=2011-5-1&offset=2&limit=2 for subject with role Create or Update or Delete or Read/Only

        rule = (Request.method == Http.GET) \
            & (Request.headers["Content-Type"] == "application/json") \
            & ( Subject.role.In(['Create', 'Update', 'Delete', 'Read/Only']) )

        self.assertTrue(rule.eval(self.request_context, {}))
        self.request_context['headers']['Content-Type'] = "application/xml"
        self.assertFalse(rule.eval(self.request_context, {}))

    def test_rule2(self):

        # Rule 2: Allow GET on /tenants/{tenantId}/servers/{serverId} if the http header "X-Tenant-Id" matches tenantId
        rule2 = (Request.method == Http.GET) \
               & (Request.url % '/tenants/{tenantId}/servers/{serverId}') \
               & (Request.url['tenantId'] == Request.headers['X-Tenant-Id'])

        rule = (Method == GET) \
               & (Url % '/tenants/{tenantId}/servers/{serverId}') \
               & (Url['tenantId'] == Headers['X-Tenant-Id'])

        self.request_context['url'] = '/tenants/T12345/servers/Scfx-123-1221-cfg-92a'
        self.assertFalse(rule.eval(self.request_context, {}))
        self.request_context['headers']['X-Tenant-Id'] = "T12345"
        self.assertTrue(rule.eval(self.request_context, {}))

