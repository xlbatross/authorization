from flask import Flask, request
from flask_restx import Api, Resource
from mediapipe.python.solutions import face_mesh as fm, drawing_utils as du, drawing_styles as ds
import base64
import numpy as np
from enum import Enum

class ResponseType(Enum):
    NONE = -1
    CLASSIFY = 1

def jsonTemplate():
    return {"type" : ResponseType.NONE.value, "attribute" : {}}

face_mesh = fm.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

image_shape = (480, 640, 3)

app = Flask(__name__)
api = Api(app)

# @api.route('/hello')
# class HelloWorld(Resource):
#     def get(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
#         return {"hello": "안녕!"}

@api.route('/classify')
class Classify(Resource):
    def post(self):
        """
        type : CLASSIFY (int)
        attribute : 
        {
            
        }
        """
        template = jsonTemplate()
        template["type"] = ResponseType.CLASSIFY.value
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