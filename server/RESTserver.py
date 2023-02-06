from flask import Flask, request
from flask_restx import Api, Resource

from mediapipe.python.solutions import face_mesh as fm, drawing_utils as du, drawing_styles as ds
import base64
import numpy as np

from database import Database
from enum import Enum

class ResponseType(Enum):
    NONE = -1
    AUTHORIZATION = 1

    GET_AREAS = 2
    INSERT_AREA = 3
    UPDATE_AREA = 4
    DELETE_AREA = 5

def responseTemplate(enumMember : ResponseType):
    return {"type" : enumMember.value, "attribute" : {}}

face_mesh = fm.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

image_shape = (480, 640, 3)

db = Database()

app = Flask(__name__)
api = Api(app)

@api.route('/areas')
class Areas(Resource):
    def get(self):
        """
        description

        input value
        - None

        return value 
        - response (json)
        {
            "type" : GET_AREAS (int),
            "attribute" : 
            {
                "result" : SUCCESS(1) or ERROR(-1) (int),
                "areas" : [{
                    "area_id" : (int),
                    "area_name" : (str)
                }] (array)
            }
        }
        """
        template = responseTemplate(ResponseType.GET_AREAS)
        template["attribute"] = db.selectAreas()
        return template
    
    def post(self):
        """
        description

        input value
        - request (json)
        {
            "name" : (str)
        }

        return value
        - response (json)
        {
            "type" : INSERT_AREA (int),
            "attribute" : 
            {
                "result" : SUCCESS(1) or FAILURE(0) or ERROR(-1) (int),
                "message" : (str)
            }
        }
        """
        param = request.get_json()
        template = responseTemplate(ResponseType.INSERT_AREA)
        if "name" in param and type(param["name"]) == str:
            template["attribute"] = db.insertArea(param["name"])
        return template

@api.route('/areas/<int:id>')
class Areas(Resource):
    def put(self, id):
        """
        description

        input value
        - url (<int: id>)
        - request (json)
        {
            "name" : (str)
        }

        return value
        - response (json)
        {
            "type" : UPDATE_AREA (int),
            "attribute" : 
            {
                "result" : SUCCESS(1) or FAILURE(0) or ERROR(-1) (int),
                "message" : (str)
            }
        }
        """
        param = request.get_json()
        template = responseTemplate(ResponseType.UPDATE_AREA)
        if "name" in param and type(param["name"]) == str:
            template["attribute"] = db.updateArea(id, param["name"])
        return template

    def delete(self, id):
        """
        description

        input value
        - url (<int: id>)

        return value
        - response (json)
        {
            "type" : DELETE_AREA (int),
            "attribute" : 
            {
                "result" : SUCCESS(1) or FAILURE(0) or ERROR(-1) (int),
                "message" : (str)
            }
        }
        """
        template = responseTemplate(type=ResponseType.DELETE_AREA)
        template["attribute"] = db.deleteArea(id)
        return template

@api.route('/authorize')
class Authorization(Resource):
    def post(self):
        """
        type : AUTHORIZATION (int),
        attribute : 
        {
            
        }
        """
        template = responseTemplate()
        template["type"] = ResponseType.AUTHORIZATION.value
        param = request.get_json()
        try:
            imageBytes = base64.b64decode(param['image'].encode())
            image : np.ndarray = np.ndarray(shape=image_shape, dtype=np.uint8, buffer=imageBytes)
            results = face_mesh.process(image)
            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                du.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=fm.FACEMESH_FACE_OVAL,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=ds.DrawingSpec((255,0,255)))
        except:
            image = np.zeros(shape=image_shape, dtype=np.uint8)
        finally:
            base64Decoding = base64.b64encode(image.data).decode()
        template["attribute"]["image"] = base64Decoding
        return template

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
