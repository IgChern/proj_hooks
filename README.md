<p align="center">
  <img src="app_hooks/static/05f2e4cd15856e724c1738711295bb1f.png" width="226">
</p>

# proj_hooks

### Описание
Проект "proj_hooks" представляет собой инструмент для обработки данных и отправки сообщений через различные эндпоинты на основе заданных фильтров.

### Структура проекта
Проект состоит из 2 модулей: app_users и app_hooks.

- app_users предназначен для создания форм и аутентификации пользователей, а так же для хранения базового шаблона и шаблонов форм.
- Основной функционал проекта находится в модуле app_hooks. Здесь реализована обработка данных и отправка сообщений в Discord через различные эндпоинты.  
В данном модуле реализованы основные компоненты:
    - base.py предоставляет абстрактный класс, который определяет общую структуру для всех эндпоинтов. Конкретные реализации эндпоинтов наследуются от этого класса и предоставляют свою собственную логику отправки сообщений.
    - discord.py реализует функционал отправки сообщений в Discord через конкретные эндпоинты.
    - middleware.py реализует middleware для статистики релизов и статистики задач. Метод process получает данные из Jira и возвращает статистику, в зависимости от типа middleware у эндпоинта.
    - models.py представляет модели для работы с данными.
    - parsers.py объявляется класс CallbackParser, с помощью которого возможно обрабатывать данные колбэка.
    - storage.py реализован интерфейс по извлечению фильтров из базы данных, которые возвращаются в списке словарей.
    - urls.py настройка маршрутов, используется декоратор login_required для защиты маршрутов, требующих аутентификации.
    - views.py определены представления для управления Ивентами и связанными с ними сущностями(эндпоинты, фильтры и т.д.)
    - webhook.py это сервис для обработки колбэков. В конструкторе инициализируется экземпляр парсера CallbackParser, который использует хранилище DjangoStorage.


## Требования для пользования приложением

Убедитесь, что Docker и Docker-Compose установлены на вашем ПК.


### 1. Склонируйте репозиторий:

    git clone https://github.com/IgChern/proj_hooks

### 2. Перейдите по пути проекта:

    cd proj_hooks

### 3. Создайте файл .env со своими собственными настройками (либо, вы можете запустить приложение локально без .env):

    POSTGRES_ENGINE=<your_settings>
    POSTGRES_NAME=<your_settings>
    POSTGRES_USER=<your_settings>
    POSTGRES_PASSWORD=<your_settings>
    POSTGRES_HOST=<your_settings>
    POSTGRES_PORT=<your_settings>

### 4. Соберите и запустите Docker контейнер:

    docker-compose build

    docker-compose up

### 5. Доступ к интерфейсу проекта:  
1. [http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/) - Страница авторизации и аутентификации
2. [http://127.0.0.1:8000/events/](http://127.0.0.1:8000/events/) - Главная страница (Необходима авторизация)

### 6. Отправка POST запроса для получения сообщения в Discord
Вам необходим JSON, который представляет собой данные колбэка от системы Jira.
<details>
  <summary>Нажмите для просмотра JSON</summary>
{
    "timestamp": 1678868043179,
    "webhookEvent": "jira:issue_created",
    "issue_event_type_name": "issue_created",
    "user": {
        "self": "https://jira.appevent.ru/rest/api/2/user?username=r.khantimirov",
        "name": "r.khantimirov",
        "key": "ug:3da0db27-d452-46e7-9ec6-91df608189ee",
        "emailAddress": "r.khantimirov@appevent.ru",
        "avatarUrls": {
            "48x48": "https://jira.appevent.ru/secure/useravatar?ownerId=ug%3A3da0db27-d452-46e7-9ec6-91df608189ee&avatarId=10701",
            "24x24": "https://jira.appevent.ru/secure/useravatar?size=small&ownerId=ug%3A3da0db27-d452-46e7-9ec6-91df608189ee&avatarId=10701",
            "16x16": "https://jira.appevent.ru/secure/useravatar?size=xsmall&ownerId=ug%3A3da0db27-d452-46e7-9ec6-91df608189ee&avatarId=10701",
            "32x32": "https://jira.appevent.ru/secure/useravatar?size=medium&ownerId=ug%3A3da0db27-d452-46e7-9ec6-91df608189ee&avatarId=10701"
        },
        "displayName": "Ринат Хантимиров",
        "active": true,
        "timeZone": "Europe/Moscow"
    },
    "issue": {
        "id": "39805",
        "self": "https://jira.appevent.ru/rest/api/2/issue/39805",
        "key": "AP-3663",
        "fields": {
            "issuetype": {
                "self": "https://jira.appevent.ru/rest/api/2/issuetype/10017",
                "id": "10017",
                "description": "A problem or error.",
                "iconUrl": "https://jira.appevent.ru/secure/viewavatar?size=xsmall&avatarId=10303&avatarType=issuetype",
                "name": "Ошибка",
                "subtask": false,
                "avatarId": 10303
            },
            "timespent": null,
            "customfield_10031": null,
            "project": {
                "self": "https://jira.appevent.ru/rest/api/2/project/10004",
                "id": "10004",
                "key": "AP",
                "name": "AppEvent",
                "projectTypeKey": "software",
                "avatarUrls": {
                    "48x48": "https://jira.appevent.ru/secure/projectavatar?pid=10004&avatarId=11002",
                    "24x24": "https://jira.appevent.ru/secure/projectavatar?size=small&pid=10004&avatarId=11002",
                    "16x16": "https://jira.appevent.ru/secure/projectavatar?size=xsmall&pid=10004&avatarId=11002",
                    "32x32": "https://jira.appevent.ru/secure/projectavatar?size=medium&pid=10004&avatarId=11002"
                }
            },
            "customfield_10032": null,
            "fixVersions": [],
            "customfield_10033": null,
            "customfield_10034": null,
            "aggregatetimespent": null,
            "resolution": null,
            "customfield_10035": null,
            "customfield_10037": null,
            "customfield_10027": null,
            "customfield_10500": null,
            "resolutiondate": null,
            "workratio": -1,
            "lastViewed": null,
            "watches": {
                "self": "https://jira.appevent.ru/rest/api/2/issue/AP-3663/watchers",
                "watchCount": 0,
                "isWatching": false
            },
            "created": "2023-03-15T11:14:03.150+0300",
            "customfield_10020": [
                "com.atlassian.greenhopper.service.sprint.Sprint@248e5c61[id=27,rapidViewId=21,state=ACTIVE,name=Спринт 22,startDate=2023-03-13T16:31:00.000+03:00,endDate=2023-03-27T16:31:00.000+03:00,completeDate=<null>,activatedDate=2023-03-13T10:13:43.625+03:00,sequence=27,goal=,autoStartStop=false,synced=false]"
            ],
            "customfield_10021": null,
            "priority": {
                "self": "https://jira.appevent.ru/rest/api/2/priority/10000",
                "iconUrl": "https://i.pinimg.com/originals/10/9e/11/109e11c6b044482c1e3a7726cf565ca5.png",
                "name": "Hot",
                "id": "10000"
            },
            "customfield_10100": null,
            "labels": [],
            "customfield_10016": null,
            "customfield_10018": null,
            "customfield_10019": "0|i00rg1:",
            "timeestimate": null,
            "aggregatetimeoriginalestimate": null,
            "versions": [],
            "issuelinks": [],
            "assignee": null,
            "updated": "2023-03-15T11:14:03.150+0300",
            "status": {
                "self": "https://jira.appevent.ru/rest/api/2/status/10011",
                "description": "",
                "iconUrl": "https://jira.appevent.ru/",
                "name": "Backlog",
                "id": "10011",
                "statusCategory": {
                    "self": "https://jira.appevent.ru/rest/api/2/statuscategory/2",
                    "id": 2,
                    "key": "new",
                    "colorName": "blue-gray",
                    "name": "К выполнению"
                }
            },
            "components": [],
            "middleware": [],
            "customfield_10050": null,
            "timeoriginalestimate": null,
            "description": null,
            "customfield_10014": null,
            "timetracking": {},
            "customfield_10015": null,
            "archiveddate": null,
            "customfield_10005": null,
            "customfield_10049": null,
            "customfield_10006": null,
            "customfield_10600": null,
            "customfield_10007": null,
            "customfield_10601": null,
            "customfield_10008": null,
            "attachment": [],
            "customfield_10009": null,
            "aggregatetimeestimate": null,
            "summary": "TEST",
            "creator": {
                "self": "https://jira.appevent.ru/rest/api/2/user?username=r.khantimirov",
                "name": "r.khantimirov",
                "key": "ug:3da0db27-d452-46e7-9ec6-91df608189ee",
                "emailAddress": "r.khantimirov@appevent.ru",
                "avatarUrls": {
                    "48x48": "https://jira.appevent.ru/secure/useravatar?ownerId=ug%3A3da0db27-d452-46e7-9ec6-91df608189ee&avatarId=10701",
                    "24x24": "https://jira.appevent.ru/secure/useravatar?size=small&ownerId=ug%3A3da0db27-d452-46e7-9ec6-91df608189ee&avatarId=10701",
                    "16x16": "https://jira.appevent.ru/secure/useravatar?size=xsmall&ownerId=ug%3A3da0db27-d452-46e7-9ec6-91df608189ee&avatarId=10701",
                    "32x32": "https://jira.appevent.ru/secure/useravatar?size=medium&ownerId=ug%3A3da0db27-d452-46e7-9ec6-91df608189ee&avatarId=10701"
                },
                "displayName": "Ринат Хантимиров",
                "active": true,
                "timeZone": "Europe/Moscow"
            },
            "subtasks": [],
            "customfield_10041": null,
            "customfield_10042": null,
            "reporter": {
                "self": "https://jira.appevent.ru/rest/api/2/user?username=r.khantimirov",
                "name": "r.khantimirov",
                "key": "ug:3da0db27-d452-46e7-9ec6-91df608189ee",
                "emailAddress": "r.khantimirov@appevent.ru",
                "avatarUrls": {
                    "48x48": "https://jira.appevent.ru/secure/useravatar?ownerId=ug%3A3da0db27-d452-46e7-9ec6-91df608189ee&avatarId=10701",
                    "24x24": "https://jira.appevent.ru/secure/useravatar?size=small&ownerId=ug%3A3da0db27-d452-46e7-9ec6-91df608189ee&avatarId=10701",
                    "16x16": "https://jira.appevent.ru/secure/useravatar?size=xsmall&ownerId=ug%3A3da0db27-d452-46e7-9ec6-91df608189ee&avatarId=10701",
                    "32x32": "https://jira.appevent.ru/secure/useravatar?size=medium&ownerId=ug%3A3da0db27-d452-46e7-9ec6-91df608189ee&avatarId=10701"
                },
                "displayName": "Ринат Хантимиров",
                "active": true,
                "timeZone": "Europe/Moscow"
            },
            "customfield_10043": null,
            "customfield_10044": null,
            "aggregateprogress": {
                "progress": 0,
                "total": 0
            },
            "customfield_10001": null,
            "customfield_10045": null,
            "customfield_10046": null,
            "customfield_10200": "{summaryBean=com.atlassian.jira.plugin.devstatus.rest.SummaryBean@bd5d09d[summary={pullrequest=com.atlassian.jira.plugin.devstatus.rest.SummaryItemBean@492bb7c3[overall=PullRequestOverallBean{stateCount=0, state='OPEN', details=PullRequestOverallDetails{openCount=0, mergedCount=0, declinedCount=0}},byInstanceType={}], build=com.atlassian.jira.plugin.devstatus.rest.SummaryItemBean@6d705880[overall=com.atlassian.jira.plugin.devstatus.summary.beans.BuildOverallBean@79f16f42[failedBuildCount=0,successfulBuildCount=0,unknownBuildCount=0,count=0,lastUpdated=<null>,lastUpdatedTimestamp=<null>],byInstanceType={}], review=com.atlassian.jira.plugin.devstatus.rest.SummaryItemBean@330d418d[overall=com.atlassian.jira.plugin.devstatus.summary.beans.ReviewsOverallBean@5aa182d9[stateCount=0,state=<null>,dueDate=<null>,overDue=false,count=0,lastUpdated=<null>,lastUpdatedTimestamp=<null>],byInstanceType={}], deployment-environment=com.atlassian.jira.plugin.devstatus.rest.SummaryItemBean@35fa7555[overall=com.atlassian.jira.plugin.devstatus.summary.beans.DeploymentOverallBean@478387d7[topEnvironments=[],showProjects=false,successfulCount=0,count=0,lastUpdated=<null>,lastUpdatedTimestamp=<null>],byInstanceType={}], repository=com.atlassian.jira.plugin.devstatus.rest.SummaryItemBean@1e5bb783[overall=com.atlassian.jira.plugin.devstatus.summary.beans.CommitOverallBean@483a49db[count=0,lastUpdated=<null>,lastUpdatedTimestamp=<null>],byInstanceType={}], branch=com.atlassian.jira.plugin.devstatus.rest.SummaryItemBean@2e8cdd54[overall=com.atlassian.jira.plugin.devstatus.summary.beans.BranchOverallBean@75ea5a6d[count=0,lastUpdated=<null>,lastUpdatedTimestamp=<null>],byInstanceType={}]},errors=[],configErrors=[]], devSummaryJson={\"cachedValue\":{\"errors\":[],\"configErrors\":[],\"summary\":{\"pullrequest\":{\"overall\":{\"count\":0,\"lastUpdated\":null,\"stateCount\":0,\"state\":\"OPEN\",\"details\":{\"openCount\":0,\"mergedCount\":0,\"declinedCount\":0,\"total\":0},\"open\":true},\"byInstanceType\":{}},\"build\":{\"overall\":{\"count\":0,\"lastUpdated\":null,\"failedBuildCount\":0,\"successfulBuildCount\":0,\"unknownBuildCount\":0},\"byInstanceType\":{}},\"review\":{\"overall\":{\"count\":0,\"lastUpdated\":null,\"stateCount\":0,\"state\":null,\"dueDate\":null,\"overDue\":false,\"completed\":false},\"byInstanceType\":{}},\"deployment-environment\":{\"overall\":{\"count\":0,\"lastUpdated\":null,\"topEnvironments\":[],\"showProjects\":false,\"successfulCount\":0},\"byInstanceType\":{}},\"repository\":{\"overall\":{\"count\":0,\"lastUpdated\":null},\"byInstanceType\":{}},\"branch\":{\"overall\":{\"count\":0,\"lastUpdated\":null},\"byInstanceType\":{}}}},\"isStale\":true}}",
            "customfield_10003": null,
            "customfield_10047": null,
            "customfield_10004": null,
            "customfield_10048": null,
            "customfield_10038": null,
            "customfield_10039": null,
            "environment": null,
            "duedate": null,
            "progress": {
                "progress": 0,
                "total": 0
            },
            "comment": {
                "comments": [],
                "maxResults": 0,
                "total": 0,
                "startAt": 0
            },
            "votes": {
                "self": "https://jira.appevent.ru/rest/api/2/issue/AP-3663/votes",
                "votes": 0,
                "hasVoted": false
            },
            "worklog": {
                "startAt": 0,
                "maxResults": 20,
                "total": 0,
                "worklogs": []
            },
            "archivedby": null
        }
    }
}
</details>  

Вы можете использовать Postman для отправки запросов по адресу.
[http://127.0.0.1:8000/jira-callback/](http://127.0.0.1:8000/jira-callback/) - Адрес для отправки POST запросов

### 7. Остановка Docker контейнера:

    docker-compose down
