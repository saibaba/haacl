import dsl
from dsl import *
import unittest

class Roles2(unittest.TestCase):

    def setUp(self):
        self.request_context =  {
            'method' : 'HEAD',
            'url' : 'http://www.service.com/ctx/path/account',
            'subject' : { 
                'role' : 'Create',
            },
        }
        dsl.dsl_debug = False

    def test_rule1(self):


        # Rule 1: Allow HEAD on /account for subject with role Create

        rule1 = (Method == HEAD) \
            & (Url / ".*/account$") \
            & ( Subject.role.In(['Create', 'Update', 'Delete', 'Read/Only']) )


        self.assertTrue(rule1.eval(self.request_context, {}))

        self.request_context['subject']['role'] = "Nobody"
        self.assertFalse(rule1.eval(self.request_context, {}))

    def test_rule2(self):

        # Rule 2: Allow POST on /account for subject with role Update

        rule2 = (Method == POST) \
            & (Url / ".*/account$") \
            & Subject.role.In(['Update'])

        self.request_context['subject']['role'] = "Update"
        self.request_context['method'] = 'POST'

        self.assertTrue(rule2.eval(self.request_context, {}))
        self.request_context['subject']['role'] = "Read/Only"
        self.assertFalse(rule2.eval(self.request_context, {}))


    def test_rule3(self):

        # Rule 3: Allow GET on /account for subject with role Read/Only

        rule3 = (Method == GET) \
            & (Url / ".*/account$") \
            & Subject.role.In(['Read/Only'])

        self.request_context['subject']['role'] = "Read/Only"
        self.request_context['method'] = 'GET'

        self.assertTrue(rule3.eval(self.request_context, {}))
        self.request_context['subject']['role'] = "Create"
        self.assertFalse(rule3.eval(self.request_context, {}))

    def test_rule4(self):

        # Rule 4: Allow PUT on /account/container for subject with role Create

        rule4 = (Method == PUT) \
            & (Url / ".*/account/container$") \
            & Subject.role.In(['Create'])

        self.request_context['url'] = "http://www.service.com/ctx/path/account/container"
        self.request_context['subject']['role'] = "Create"
        self.request_context['method'] = 'PUT'

        self.assertTrue(rule4.eval(self.request_context, {}))
        self.request_context['subject']['role'] = "Read/Only"
        self.assertFalse(rule4.eval(self.request_context, {}))

    def test_rule5(self):

        # Rule 5: Allow DELETE on /account/container for subject with role Delete

        rule5 = (Method == DELETE) \
            & (Url / ".*/account/container$") \
            & Subject.role.In(['Delete'])

        self.request_context['url'] = "http://www.service.com/ctx/path/account/container"
        self.request_context['subject']['role'] = "Delete"
        self.request_context['method'] = 'DELETE'

        self.assertTrue(rule5.eval(self.request_context, {}))
        self.request_context['subject']['role'] = "Read/Only"
        self.assertFalse(rule5.eval(self.request_context, {}))

    def test_rule6(self):

        # Rule 6: Allow HEAD on /account/container for subject with role Read/Only

        rule6 = (Method == HEAD) \
            & (Url / ".*/account/container$") \
            & Subject.role.In(['Read/Only'])

        self.request_context['url'] = "http://www.service.com/ctx/path/account/container"
        self.request_context['subject']['role'] = "Read/Only"
        self.request_context['method'] = 'HEAD'

        self.assertTrue(rule6.eval(self.request_context, {}))
        self.request_context['subject']['role'] = "Create"
        self.assertFalse(rule6.eval(self.request_context, {}))

    def test_rule7(self):

        # Rule 7: Allow POST on /account/container for subject with role Update

        rule7 = (Method == POST) \
            & (Url / ".*/account/container$") \
            & Subject.role.In(['Update'])

        self.request_context['url'] = "http://www.service.com/ctx/path/account/container"
        self.request_context['subject']['role'] = "Update"
        self.request_context['method'] = 'POST'

        self.assertTrue(rule7.eval(self.request_context, {}))
        self.request_context['method'] = "DELETE"
        self.assertFalse(rule7.eval(self.request_context, {}))

    def test_rule8(self):

        # Rule 8: Allow GET on /account/container for subject with role Read/Only

        rule8 = (Method == GET) \
            & (Url / ".*/account/container$") \
            & Subject.role.In(['Read/Only'])

        self.request_context['url'] = "http://www.service.com/ctx/path/account/container"
        self.request_context['subject']['role'] = "Read/Only"
        self.request_context['method'] = 'GET'

        self.assertTrue(rule8.eval(self.request_context, {}))
        self.request_context['method'] = "DELETE"
        self.assertFalse(rule8.eval(self.request_context, {}))

    def test_rule9(self):

        # Rule 10: Allow GET on /account/container/object for subject with role Read/Only

        rule = (Method == GET) \
            & (Url / ".*/account/container/object$") \
            & Subject.role.In(['Read/Only'])

        self.request_context['url'] = "http://www.service.com/ctx/path/account/container/object"
        self.request_context['subject']['role'] = "Read/Only"
        self.request_context['method'] = 'GET'

        self.assertTrue(rule.eval(self.request_context, {}))
        self.request_context['subject']['role'] = "Update"
        self.assertFalse(rule.eval(self.request_context, {}))

    def test_rule10(self):

        # Rule 11: Allow PUT on /account/container/object for subject with role Create or Update or Delete

        rule = (Method == PUT) \
            & (Url / ".*/account/container/object$") \
            & Subject.role.In(['Create', 'Update', 'Delete'])

        self.request_context['url'] = "http://www.service.com/ctx/path/account/container/object"
        self.request_context['subject']['role'] = "Create"
        self.request_context['method'] = 'PUT'

        self.assertTrue(rule.eval(self.request_context, {}))
        self.request_context['subject']['role'] = "Read/Only"
        self.assertFalse(rule.eval(self.request_context, {}))

    def test_rule11(self):

        # Rule 12: Allow PUT on /account/container/destobject for subject with role Create or Update or Delete

        rule = (Method == PUT) \
            & (Url / ".*/account/container/destobject$") \
            & Subject.role.In(['Create', 'Update', 'Delete'])

        self.request_context['url'] = "http://www.service.com/ctx/path/account/container/destobject"
        self.request_context['subject']['role'] = "Create"
        self.request_context['method'] = 'PUT'

        self.assertTrue(rule.eval(self.request_context, {}))
        self.request_context['subject']['role'] = "Read/Only"
        self.assertFalse(rule.eval(self.request_context, {}))

    def test_rule12(self):

        # Rule 13: Allow DELETE on /account/container/object for subject with role Create or Update or Delete

        rule = (Method == DELETE) \
            & (Url / ".*/account/container/object$") \
            & Subject.role.In(['Create', 'Update', 'Delete'])

        self.request_context['url'] = "http://www.service.com/ctx/path/account/container/object"
        self.request_context['subject']['role'] = "Create"
        self.request_context['method'] = 'DELETE'

        self.assertTrue(rule.eval(self.request_context, {}))
        self.request_context['subject']['role'] = "Read/Only"
        self.assertFalse(rule.eval(self.request_context, {}))

    def test_rule13(self):

        # Rule 14: Allow HEAD on /account/container/object for subject with role Read/Only

        rule = (Method == HEAD) \
            & (Url / ".*/account/container/object$") \
            & Subject.role.In(['Read/Only'])

        self.request_context['url'] = "http://www.service.com/ctx/path/account/container/object"
        self.request_context['subject']['role'] = "Read/Only"
        self.request_context['method'] = 'HEAD'

        self.assertTrue(rule.eval(self.request_context, {}))
        self.request_context['subject']['role'] = "Create"
        self.assertFalse(rule.eval(self.request_context, {}))

    def test_rule14(self):

        # Rule 15: Allow POST on /account/container/object for subject with role Create or Update or Delete

        rule = (Method == POST) \
            & (Url / ".*/account/container/object$") \
            & Subject.role.In(['Create', 'Update', 'Delete'])

        self.request_context['url'] = "http://www.service.com/ctx/path/account/container/object"
        self.request_context['subject']['role'] = 'Update'
        self.request_context['method'] = 'POST'

        self.assertTrue(rule.eval(self.request_context, {}))
        self.request_context['subject']['role'] = "Read/Only"
        self.assertFalse(rule.eval(self.request_context, {}))

