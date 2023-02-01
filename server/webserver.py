from flask import Flask, request
from flask_restx import Api, Resource
import base64
import numpy as np
from mediapipe.python.solutions import face_mesh as fm, drawing_utils as du, drawing_styles as ds

face_mesh = fm.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

app = Flask(__name__)
api = Api(app)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        return {"hello": "안녕!"}

@api.route('/classify')
class Classify(Resource):
    def post(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        param = request.get_json()
        image : np.zeros(shape=(480, 640, 3), dtype=np.uint8)
        if 'image' in param:
            imageBytes = base64.b64decode(param['image'].encode())
            image : np.ndarray = np.ndarray(shape=(480, 640, 3), dtype=np.uint8, buffer=imageBytes)
            results = face_mesh.process(image)
            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                du.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=fm.FACEMESH_FACE_OVAL,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=ds.DrawingSpec((255,0,255)))
        base64Decoding = base64.b64encode(image.data).decode()
        return {"image": base64Decoding}    

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)