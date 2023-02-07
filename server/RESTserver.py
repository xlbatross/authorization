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
    GET_AREA = 3
    INSERT_AREA = 4
    UPDATE_AREA = 5
    DELETE_AREA = 6

    GET_SECTORS = 7
    GET_SECTOR = 8
    INSERT_SECTOR = 9
    UPDATE_SECTOR = 10
    DELETE_SECTOR = 11

    GET_LEVELS = 12

    GET_USERS = 13
    GET_USER = 14
    INSERT_USER = 15
    UPDATE_USER = 16
    DELETE_USER = 17

    GET_AREA_LOGS = 18
    GET_SECTOR_LOGS = 19
    GET_USER_LOGS = 20

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

@api.route('/levels')
class Levels(Resource):
    def get(self):
        """
        description

        input value
        - None

        return value 
        - response (json)
        {
            "type" : GET_LEVELS (int),
            "attribute" : 
            {
                "result" : SUCCESS(1) or ERROR(-1) (int),
                "levels" : [{
                    "level_id" : (int),
                    "level_value" : (int)
                }] (array)
            }
        }
        """
        template = responseTemplate(ResponseType.GET_LEVELS)
        template["attribute"] = db.selectLevels()
        return template

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
            "name" : (str),
            "address" : (str)
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
        if "name" in param and type(param["name"]) == str and "address" in param and type(param["address"]) == str:
            template["attribute"] = db.insertArea(param["name"], param["address"])
        return template

@api.route('/areas/<int:id>')
class Areas(Resource):
    def get(self, id):
        """
        description

        input value
        - url (<int: id>)

        return value
        - response (json)
        {
            "type" : GET_AREA (int),
            "attribute" : 
            {
                "result" : SUCCESS(1) or ERROR(-1) (int),
                "area" : {
                    "area_name" : (str),
                    "area_address" : (str)
                }
            }
        }
        """
        template = responseTemplate(ResponseType.GET_AREA)
        template["attribute"] = db.selectArea(id)
        return template

    def put(self, id):
        """
        description

        input value
        - url (<int: id>)
        - request (json)
        {
            "name" : (str),
            "address" : (str)
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
        if "name" in param and type(param["name"]) == str and "address" in param and type(param["address"]) == str:
            template["attribute"] = db.updateArea(id, param["name"], param["address"])
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

@api.route('/areas/<int:id>/sectors')
class AreaSectors(Resource):
    def get(self, id):
        """
        description

        input value
        - url (<int: id>)

        return value 
        - response (json)
        {
            "type" : GET_SECTORS (int),
            "attribute" : 
            {
                "result" : SUCCESS(1) or ERROR(-1) (int),
                "sectors" : [{
                    "sector_id" : (int),
                    "sector_name" : (str)
                }] (array)
            }
        }
        """
        template = responseTemplate(ResponseType.GET_SECTORS)
        template["attribute"] = db.selectSectors(id)
        return template
    
    def post(self, id):
        """
        description

        input value
        - url (<int: id>)
        - request (json)
        {
            "levelId" : (int),
            "name" : (str)
        }

        return value 
        - response (json)
        {
            "type" : INSERT_SECTOR (int),
            "attribute" : 
            {
                "result" : SUCCESS(1) or FAILURE(0) or ERROR(-1) (int),
                "message" : (str)
            }
        }
        """
        param = request.get_json()
        template = responseTemplate(ResponseType.INSERT_SECTOR)
        if "levelId" in param and type(param["levelId"]) == int and "name" in param and type(param["name"]) == str:
            template["attribute"] = db.insertSector(id, param["levelId"], param["name"])
        return template

@api.route('/sectors/<int:id>')
class Sectors(Resource):
    def get(self, id):
        """
        description

        input value
        - url (<int: id>)

        return value 
        - response (json)
        {
            "type" : GET_SECTOR (int),
            "attribute" : 
            {
                "result" : SUCCESS(1) or ERROR(-1) (int),
                "sector" : {
                    "sector_name" : (str),
                    "level_id" : (int),
                    "level_value" : (int)
                }
            }
        }
        """
        template = responseTemplate(ResponseType.GET_SECTOR)
        template["attribute"] = db.selectSector(id)
        return template
    
    def put(self, id):
        """
        description

        input value
        - url (<int: id>)
        - request (json)
        {
            "levelId" : (int),
            "name" : (str)
        }

        return value 
        - response (json)
        {
            "type" : UPDATE_SECTOR (int),
            "attribute" : 
            {
                "result" : SUCCESS(1) or FAILURE(0) or ERROR(-1) (int),
                "message" : (str)
            }
        }
        """
        param = request.get_json()
        template = responseTemplate(ResponseType.UPDATE_SECTOR)
        if "levelId" in param and type(param["levelId"]) == int and "name" in param and type(param["name"]) == str:
            template["attribute"] = db.updateSector(id, param["levelId"], param["name"])
        return template
    
    def delete(self, id):
        """
        description

        input value
        - url (<int: id>)

        return value
        - response (json)
        {
            "type" : DELETE_SECTOR (int),
            "attribute" : 
            {
                "result" : SUCCESS(1) or FAILURE(0) or ERROR(-1) (int),
                "message" : (str)
            }
        }
        """
        template = responseTemplate(type=ResponseType.DELETE_SECTOR)
        template["attribute"] = db.deleteSector(id)
        return template

@api.route('/area/<int:id>/users')
class AreaUsers(Resource):
    def get(self, id):
        """
        description

        input value
        - url (<int: id>)

        return value 
        - response (json)
        {
            "type" : GET_USERS (int),
            "attribute" : 
            {
                "result" : SUCCESS(1) or ERROR(-1) (int),
                "users" : [{
                    "user_id" : (int),
                    "user_name" : (str)
                }] (array)
            }
        }
        """
        template = responseTemplate(ResponseType.GET_USERS)
        template["attribute"] = db.selectUsers(id)
        return template
    
    def post(self, id):
        """
        description

        input value
        - url (<int: id>)
        - request (json)
        {
            "levelId" : (int),
            "name" : (str),
            "image" : (base64),
            "phone" : (str)
        }

        return value 
        - response (json)
        {
            "type" : INSERT_USER (int),
            "attribute" : 
            {
                "result" : SUCCESS(1) or FAILURE(0) or ERROR(-1) (int),
                "message" : (str)
            }
        }
        """
        param = request.get_json()
        template = responseTemplate(ResponseType.INSERT_USER)
        try:
            imageBytes = base64.b64decode(param['image'].encode())
            image : np.ndarray = np.ndarray(shape=image_shape, dtype=np.uint8, buffer=imageBytes)
            results = face_mesh.process(image)
            if results.multi_face_landmarks:
                imagePath = "/photo"
                template["attribute"] = db.insertUser(id, param["levelId"], param["name"], imagePath, param["phone"])
            else:
                pass
        except:
            pass
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
        param = request.get_json()
        template = responseTemplate(ResponseType.AUTHORIZATION)
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
