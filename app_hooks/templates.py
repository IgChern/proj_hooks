from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

template_env = Environment(
    loader=FileSystemLoader('./templates'),
)


def render_to_string(template: str, base_data: dict, jira_data: dict) -> str:

    try:
        template_obj = template_env.get_template(template)
    except TemplateNotFound:
        return f'template "{template}" for filter #{base_data["id"]} dont found'

    rendered_page = template_obj.render(
        base_data=base_data,
        jira_data=jira_data,
    )

    return rendered_page
