from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_restful import Api

from index_resource import Index
from office_api_resource import (OfficeData, OfficeFinishedWorkingFor,
                                 OfficeStartWorkingFor)
from person_api_resource import (ChangePersonName, CreatePersons,
                                 PersonHappyBirthday, Persons)

# creating the flask app
app = Flask(__name__)
bootstrap = Bootstrap(app)

# support secure cross-origin requests,data transfer between browsers & servers
CORS(app, resources={r"/*": {"origins": "*"}})

# creating an API object
api = Api(app)


# adding the defined resources along with their corresponding urls
api.add_resource(Index, "/")

# Person API resources
api.add_resource(Persons, "/api/persons")
api.add_resource(CreatePersons, "/api/persons/create")
api.add_resource(ChangePersonName, "/api/persons/change-person-name")
api.add_resource(PersonHappyBirthday, "/api/persons/happy-birthday")

# Office API resources
api.add_resource(OfficeData, "/api/office")
api.add_resource(OfficeStartWorkingFor, "/api/office/add/start-working-for")
api.add_resource(
    OfficeFinishedWorkingFor,
    "/api/office/remove/finished_working_for/<int:employee_id>",
)

# driver function, threaded used to handle multiple requests
if __name__ == "__main__":
    app.run(debug=True, threaded=True)
