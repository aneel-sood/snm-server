## Project Overview

Service Needs Marketplace is an application conceived of by the [Centre for Social Services Engineering](http://csse.utoronto.ca/) at the University of Toronto. Its meant to be used by Canadian newcomer settlement service providers (e.g. JIAS Toronto, North York Community House, YMCA, etc.), to help them match newcomers to Canada with the resources (both services and goods) they need access to.

This code base, together with [snm-client](https://github.com/leonL/snm-client), is an MVP implementation of the app. As of this writing the CSSE is using a [staging deployment](https://secret-island-33471.herokuapp.com/clients/) of it as part of their pitch to service providers and other interested parties.

## Running SNM in your development environment

This web server API is built using Django and Django REST Framework, in Python 3. If you are new to Python or Django, you will likely have a lot less trouble getting a local instance of the server running by deploying it in an [isolated Python environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Note that the web server is configured to use a PostgreSQL database that supports PostGIS.

## If you are a developer building on this code...

### Consider a refactor of the Views and Serializers before adding to them or writing new code that relies upon them significantly 

This project was started by a developer new to both Django and Django REST Framework. A few different patterns were used to implement `views` and the `serializers` they rely on before one was settled on. The `ClientDetail / ClientList` view classes and there related serializers are examples of the most current and sensible pattern used to define a full complement of RESTful actions for a given resource. Refactoring the other endpoints and writing all future ones in a similar fashion is highly recommended. For more information about these patterns see the [Django REST Framework documentation](http://www.django-rest-framework.org). 

### Make note of the following decisions that informed the implementation, and that may need to be revisited

#### There are no tests as yet

This was a questionable sacrifice made in the name of building the MVP as quickly as possible. Note that the code base has reached the threshold where a developer familiar with it might be able to anticipate all the consequences of making changes or adding to it. Tests should be added to the repo ASAP.

#### Database & Model Validations

Models and their corresponding database tables were defined with very liberal validations on account of there was no business domain stakeholders to inform common and edge cses related to the data. If and when implementing validations consider whether they should be at the level of the REST Framework serializer before doing so.

#### `INSTALLED_APPS` 

No modules were removed from the `INSTALLED_APPS` array in `setting.py`. It's likely some of the default modules still included are unnecessary to this project on account of the web server returns data exclusively (as JSON predominantly, but in a couple of cases it deals with CSVs).