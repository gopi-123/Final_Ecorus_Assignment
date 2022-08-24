from flask import Response
from flask_restful import Resource


class Index(Resource):
    """ To show home page"""

    def get(self) -> Response:
        return Response("<h1> Welcome to the Site!</h1>")
