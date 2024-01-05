from django.test import TestCase

# Create your tests here.


def get_discord_data(self, jira_data: dict):

    data = dict()

    data['embeds'][0]['title'] = self.title  # Как получить key и summary?
    data['embeds'][0]['description'] = self.description
    data['embeds'][0]['url'] = self.url
    data['embeds'][0]['color'] = self.color
    data['embeds'][0]['thumbnail'] = {
        'url': self.thumbnail['url'],
        'height': self.thumbnail['height'],
        'width': self.thumbnail['width']
    }
    data['embeds'][0]['author'] = {'name': self.author['name']}
    data['embeds'][0]['footer'] = {
        'text': self.footer['text'],
        'icon_url': self.footer['icon_url']
    }

    fields = []
    for field in self.fields.all():
        field_data = {
            'name': field.name,
            'inline': field.inline
        }

        if field.value:
            field_data['value'] = field.value

        fields.append(field_data)

    data['embeds'][0]['fields'] = fields

    return data


'{{issue, fields, customfield_10500, displayName}}'
