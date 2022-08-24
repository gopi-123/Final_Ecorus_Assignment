from flask import Response, render_template, request
from flask_restful import Resource

from persons_table import (create_persons_db_table, get_persons, insert_person,
                           update_birthday_age, update_person_name)


class Persons(Resource):
    def __init__(self) -> None:
        create_persons_db_table()

    def get(self) -> Response:
        """ retrieves all person records """

        persons_list = get_persons()

        return Response(
            render_template(
                "person.html", result_user=persons_list, mimetype="text/html"
            )
        )


class CreatePersons(Resource):
    def __init__(self) -> None:
        create_persons_db_table()

    def post(self) -> Response:
        """ create / add person to the person table"""

        # receive person json object (from postman App) in format:
        # { "name": "eduardo",  "age": 29}
        # orcall assignment1 Personobject like "Person("Eduardo", 20).__dict__"

        person_dict = request.get_json()
        return Response(
            render_template(
                "createdperson.html",
                result_dict=insert_person(person_dict),
                mimetype="text/html",
            )
        )


class ChangePersonName(Resource):
    def __init__(self) -> None:
        create_persons_db_table()

    def put(self) -> Response:

        # change person by name for given person id(object_id) in format:
        # {"person_id" : 7,"name": "777new_eduardo33","age": 88}
        person_dict = request.get_json()

        return Response(
            render_template(
                "changepersonname.html",
                result_dict=update_person_name(person_dict),
                mimetype="text/html",
            )
        )


class PersonHappyBirthday(Resource):
    def __init__(self) -> None:
        create_persons_db_table()

    def put(self) -> Response:
        person_dict = request.get_json()

        return Response(
            render_template(
                "personbirthday.html",
                result_dict=update_birthday_age(person_dict),
                mimetype="text/html",
            )
        )
