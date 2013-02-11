from dsl import *
import dsl

import unittest
import collections


class Sample(unittest.TestCase):

    def setUp(self):
        dsl.dsl_debug = False

    def test_1(self):
        sample_rule = Subject.id / "[^@]+@med.example.com"

        request_context = { 'subject' : { 'id' : 'sai@med.example.com', 'attributes': { 'a' : 1 } } }
        assert sample_rule.eval(request_context, {}) == True

        request_context = { 'subject' : { 'id' : 'sai@tech.example.com', 'attributes': { 'a' : 1 } } }
        assert sample_rule.eval(request_context, {}) == False

    def test_2(self):

        rule1 = (Method == GET) \
               & (Url % ".*/service/record/medical$") \
               & (ResourceContent.path("$..record.patient.patient-number") == Subject.attributes['patient-number'] )

        rule2 = (Method == GET) \
               & ( (ResourceContent.path("$..record.patient.parent") == Subject.attributes['parent'] ) \
                   | (ResourceContent.path("$..record.patient.guardian-id") == Subject.attributes['guardian-id'] ) ) \
               & (ResourceContent.path("$..record.patient.age") < 16)

        rule3 = (Method == PUT) \
                & (Url / ".*/record/medical$") \
                & ( (ResourceContent.path("$..record.patient.parent") == Subject.attributes['parent'] ) \
                   | (ResourceContent.path("$..record.patient.guardian-id") == Subject.attributes['guardian-id'] ) ) \
                & (Subject.role.In(['physician'])) \
                & (ResourceContent.path("$..record.primaryCarePhysician.registrationID") == Subject.attributes['physician-id'] ) \
                & (ResourceContent.path("$..record.patient.age") < 16)

        rule4 = ((Method == PUT) | (Method == GET)) \
                & (Url / ".*/record/medical$") \
                & (Subject.role.In(['administrator']))

        request_context = {
            'method' : 'GET',
            'url' : 'http://www.mws.com/service/record/medical',
            'subject' : { 'id' : 'sai@tech.example.com', 'attributes': { 'a' : 1, 'patient-number' : 123, 'parent' : '001', 'physician-id' : 'Dr. X' },
                'role' : 'physician' },
            'resource': { 'content' : { 'record' : { 'patient' : { 'age': 15, 'patient-number'  : 123 }, 
                'primaryCarePhysician' : { 'registrationID' : 'Dr. X' }
                }}},
        }
        assert rule1.eval(request_context, {}) == True
        request_context['resource']['content']['record']['patient']['patient-number'] = 124
        assert rule1.eval(request_context, {}) == False


        request_context['resource']['content']['record']['patient']['patient-number'] = 220

        policy = Policy(collections.OrderedDict([ (rule1 , Allow), (rule2 , Allow), (rule3 , Allow), (rule4 , Deny)]), AllowOverrides)

        assert policy.eval(request_context) == False
        request_context['resource']['content']['record']['patient']['parent'] = '001'
        assert policy.eval(request_context) == True

        request_context['method'] = Http.PUT
        assert policy.eval(request_context) == True

        request_context['url'] = "http://www.service.com/record/medicalx"
        assert policy.eval(request_context) == False

        request_context['url'] = "http://www.service.com/record/medical"
        request_context['subject']['role'] = "administrator"
        assert policy.eval(request_context) == False

        request_context['method'] = PUT
        assert policy.eval(request_context) == False



"""

Rule 3:
=> { decision = Allow , obligations=[email] }   //TODO expand email to include from/to etc.,

"""
