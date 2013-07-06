import jinja2

from .meta import templates_path, template_extensions


_jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_path),
                                extensions=template_extensions)


def get_template(template_name):
    """Search a template.

    :param template_name: Name of the template to search for.

    :return: Template object.
    """
    return _jinja_env.get_template(template_name)
