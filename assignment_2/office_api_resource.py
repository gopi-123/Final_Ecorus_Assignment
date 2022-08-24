from flask import Response, jsonify, render_template, request
from flask_restful import Resource

from office_table import (create_office_db_table, delete_employee_by_id,
                          get_office_data, insert_office)


class OfficeData(Resource):
    def __init__(self) -> None:
        create_office_db_table()

    def get(self) -> Response:

        office_data_list = get_office_data()

        return Response(
            render_template(
                "office.html", result_office=office_data_list,
                mimetype="text/html"
            )
        )


class OfficeStartWorkingFor(Resource):
    def __init__(self) -> None:
        create_office_db_table()

    def post(self) -> Response:
        """
        create/add person working to office table
        Either take data from implemented classes or from Postman Body in
        jsonformat object= {"name": "ecorus","people_working": {"shiva": 21}}
        """

        office_dict = request.get_json()

        return Response(
            render_template(
                "officecreated.html",
                result_office=insert_office(office_dict),
                mimetype="text/html",
            )
        )


class OfficeFinishedWorkingFor(Resource):
    def __init__(self) -> None:
        create_office_db_table()

    def delete(self, employee_id) -> Response:
        """
        Delete reocrd from office table by removing person from people_working
        """
        message_dict = delete_employee_by_id(employee_id)

        if message_dict["status"] == "Employee deleted successfully":
            office_data_list = get_office_data()
            return Response(
                render_template(
                    "office.html",
                    result_office=office_data_list, mimetype="text/html"
                )
            )

        else:
            return jsonify(message_dict)
