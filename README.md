# Django Webhook for Discord



### Prerequisites

Make sure you have Docker and Docker Compose installed on your machine.

## Getting Started

### 1. Clone the repository:

    git clone https://github.com/IgChern/proj_hooks

### 2. Change directory:

    cd proj_hooks

### 3. Make .env file with your own settings (or you can use it locally without .env):

    POSTGRES_ENGINE=<your_settings>
    POSTGRES_NAME=<your_settings>
    POSTGRES_USER=<your_settings>
    POSTGRES_PASSWORD=<your_settings>
    POSTGRES_HOST=<your_settings>
    POSTGRES_PORT=<your_settings>

### 4. Build and run the Docker containers:

    docker-compose build

    docker-compose up

### 5. Access the Django development server at:  
1. [http://127.0.0.1:8000/api/filter/](http://127.0.0.1:8000/api/filter/) - Storing for filters
2. [http://127.0.0.1:8000/api/event/](http://127.0.0.1:8000/api/event/) - Storing for events

### 6. Check dictionary in Python shell:

from app_hooks.models import Filters
filters_objects = Filters.objects…all()
for obj in filters_objects:
    print(obj.make_dict())

### 7. Check DataBase locally with password 'postgres':

    psql -h localhost -U postgres -d postgres -p 5432

### 8. Stop Docker containers:

    docker-compose down
### 9. JSON Filter example and template for user:

{
        "id": 0,
        "name": "Создание задачи с приоритетом HOT в Appevent",
        "filters": [
            {"key": ["webhookEvent"], "list_key": null, "value": ["jira:issue_created"]},
            {"key": ["issue_event_type_name"], "list_key": null, "value": ["issue_created"]},
            {"key": ["issue", "fields", "project", "name"], "list_key": null, "value": ["AppEvent"]},
            {"key": ["issue", "fields", "priority", "name"], "list_key": null, "value": ["Hot"]},
            {"key": ["issue", "fields", "issuetype", "subtask"], "list_key": null, "value": [false]}
        ],
        "endpoint": "discord_embeded",
        "template": "created_default",
        "callback": "https://discordapp.com/api/webhooks/1086261129547878430/3gXse0GjXbg1EZHWsVCeP7-qF3pK08ZkjUEu-pC6u3wW_QNHkycftigVyAp6i_f78zQT"
        }

**{{ jira_data.appbuild.app_name }}**
Подготовка нового приложения к сборке: **{{ jira_data.appbuild.status }}** :white_check_mark:
[{{ jira_data.appbuild.build_url }}]
[{{ jira_data.appbuild.branch_url }}]





## Developer Information

Feel free to contact me for any questions or issues.

<a href="https://t.me/Igareokay" >
<img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/>
</a>
<a href="mailto:igchern95@gmail.com" >
<img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white"/>
</a>