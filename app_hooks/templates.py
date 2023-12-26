from jinja2 import Environment,  BaseLoader

template_env = Environment(loader=BaseLoader)


def render_to_string(template: str, base_data: dict, jira_data: dict) -> str:

    template_obj = template_env.from_string(template)

    rendered_page = template_obj.render(
        base_data=base_data,
        jira_data=jira_data,
    )

    return rendered_page
