import webapp2

from .meta import DEBUG
from .templating import get_template


class RequestHandler(webapp2.RequestHandler):
    """Base request handler suitable for customization and
    to avoid webapp2 api coupling.
    """


class TemplateRequestHandler(RequestHandler):
    """Templating related request handler."""
    def get_template(self, template_name):
        """Get a template by name.

        :param template_name: Name of the template as string.

        :return: A template object.
        """
        return get_template(template_name)

    def render(self, template_name, **context):
        """Render a template.

        :param template_name: Name of the template as string.
        :param \*\*context: Values for the template slots.
        
        :return: String representing the template rendered.
        """
        template = self.get_template(template_name)
        return template.render(**context)

    def render_to_response(self, template_name, **context):
        """Render a template and write the result to the response's body.

        :param template_name: Name of the template as string.
        :param \*\*context: Values for the template slots.
        """
        self.response.write(self.render(template_name, **context))


class WSGIApplication(webapp2.WSGIApplication):
    def __init__(self, routes=None, debug=None, config=None):
        if debug is None:
            debug = DEBUG
        super(WSGIApplication, self).__init__(routes, debug, config)


def view(f, handler_class=None, accept_method=None):
    """Request handler factory.

    It returns a response with the body set to the value returned by
    the decorated function.

    :param f: Decorated/wrapped function. This function must accept
    a parameter that is a reference to the request handler object.

    :param accept_method: Accepted request method. Default is ``get``.
    You can also pass a tuple with all the accepted methods.

    :return: :class:`RequestHandler` object.
    """
    if accept_method is None:
        accept_method = ('get',)
    if handler_class is None:
        handler_class = RequestHandler
    def handler_method(self, *args, **kwargs):
        result = f(self, *args, **kwargs)
        if result:
            self.response.write(result)
    namespace = {}
    for method in accept_method:
        namespace[method] = handler_method
    return type('ViewHandler', (handler_class,), namespace)
