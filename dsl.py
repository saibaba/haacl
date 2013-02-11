import jsonpath
import re
import operator

debug = True

def convert_template_to_regex(template):
    tre = re.compile('(\{([^/]+)\})')
    matches = tre.findall(template)
    formats = {}
    for ts,s in matches:
        formats[s] = "(?P<%s>[^/]+)" % (s)

    
    rexpr =  template.format(**formats)

    r = re.compile(rexpr)

    if debug:
        print "Template %s converted to regex: %s" % (template, rexpr)

    return r

def Eq(l, r, env):
    return operator.eq(l, r)

def And(l, r, env):
    return operator.and_(l, r)

def Or(l, r, env):
    return operator.or_(l, r)

def Lt(l, r, env):
    return operator.lt(l, r)

def Re(s, regex, env):
    if debug:
        print "Re Matching string %s for re %s" % (s, regex)
    return re.match(regex, s) is not None

def In(v, l, env):
    return v in l

def Te(url, tregex, env):
    
    matches = tregex.match(url)
    if matches is not None:
        env['url_template_params'] = matches.groupdict()

    return matches is not None
    
class BinaryPredicate(object):

    def __init__(self, p1, p2, op):
        self.p1 = p1
        self.p2 = p2
        self.op = op

    def __and__(self, p2):
        return BinaryPredicate(self, p2, And)

    def __or__(self, p2):
        return BinaryPredicate(self, p2, Or)

    def _eval(self, request_context, p, env):
        if callable(p):
            return p(request_context, env)
        else:
            return p

    def __call__(self, request_context, env):
        return self.eval(request_context, env)

    def eval(self, request_context, env):
        r1 = self._eval(request_context, self.p1, env)
        r2 = self._eval(request_context, self.p2, env)

        global debug
        if debug:
            print "EVAL:"
            print "\tp1 =", self.p1
            print "\tp2 =", self.p2
            print "\treq =", request_context 
            print "\tr1 =", r1
            print "\tr2 =", r2
            print "\top =", self.op

        if r1 is None and r2 is None:
            return False

        r = self.op(r1, r2, env)
        if debug:
            print "\tresult = ", r

        return r

class ContextField(object):

    def __init__(self):
        self.is_json = False
        self.access_path = []
        self.field_name = None
        self.use_env = False
        self.env_param = None

    def __str__(self):
        return "ContextField(field_name=%s): access_path=%s" % (self.field_name, ";".join(self.access_path))

    def __eq__(self, p2):
        return BinaryPredicate(self, p2, Eq)

    def __and__(self, p2):
        return BinaryPredicate(self, p2, And)

    def __or__(self, p2):
        return BinaryPredicate(self, p2, Or)

    def __lt__(self, p2):
        return BinaryPredicate(self, p2, Lt)

    def __div__(self, rexpr):
        return BinaryPredicate(self, rexpr, Re)

    # Request.url % template
    def __mod__(self, template):
        template_rexpr = convert_template_to_regex(template)
        return BinaryPredicate(self, template_rexpr, Te)

    def __getitem__(self, n):
        print "**** getitem called for %s on %s" % (n, str(self))
        self.field_name = n
        print "\t**** getitem called for %s on %s" % (n, str(self))
        return self

    def __getattr__(self, n):
        self.access_path.append(n)
        return self

    def path(self, path_expr):
        self.value = path_expr
        self.is_json = True
        return self

    def In(self, l):
        return BinaryPredicate(self, l, In)

    def use_env_param(self, env_param):
        self.use_env = True
        self.env_param = env_param
        return self

    def __call__(self, request_context, env):

        root = None

        p = request_context
        l = len(self.access_path)

        for i in range(l):
            n = self.access_path[i]
            print "\nTrying to extract", n, "from",  p
            if n in p:
                p = p[n]
            else:
                p = None
                break

        if self.use_env and self.env_param in env and self.field_name in env[self.env_param]:
            p = env[self.env_param][self.field_name]
        elif self.field_name is not None and p is not None and self.field_name in p:
            p = p[self.field_name]

        root = p

        if self.is_json:
            if debug:
                print "jsonpath context: ", root
                print "\tpath: ", self.value

            root = jsonpath.jsonpath(root, self.value)

            if debug:
                print "\tjsonpath result: ", root
                print "\tpath: ", self.value

            if not root:
                root = None
            else:
                root = root[0]

        print "Call returns: " , root
        return root

    def eval(self, request_context, env):
        return self(request_context, env)

class Context(object):

    def __init__(self, start_field = None):
        self.field_name =  start_field

    def __getattr__(self, n):

        context_field = ContextField()

        if self.field_name is not None:
            getattr(context_field, self.field_name)

        r = getattr(context_field, n)

        return r


class Http(object):
    GET = "GET"
    PUT = "PUT"
    POST = "POST"
    HEAD = "HEAD"
    DELETE = "DELETE"
    ContentType = "Content-Type"

Subject  = Context('subject')
Resource = Context('resource')
Request  = Context()

Http = Http()

class MethodContext(object):

    def __eq__(self, rhs):
        context_field = ContextField()
        getattr(context_field, 'method')
        return context_field == rhs

class UrlContext(object):

    def __getitem__(self, name):
        context_field = ContextField()
        getattr(context_field, 'url')
        r = context_field[name]
        r = r.use_env_param('url_template_params')
        return r

    def __mod__(self, rhs):
        context_field = ContextField()
        getattr(context_field, 'url')
        return context_field % rhs

class HeadersContext(object):
    def __getitem__(self, name):
        context_field = ContextField()
        getattr(context_field, 'headers')
        return context_field[name]

class ResourceHeadersContext(object):
    def __getitem__(self, name):
        context_field = ContextField()
        getattr(context_field, 'resource')
        return context_field['headers']

Method = MethodContext()
Url = UrlContext()
Headers = HeadersContext()
ResourceHeaders = ResourceHeadersContext()

GET = "GET"

