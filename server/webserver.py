from flask import Flask
from flask_restx import Api, Resource
import json
app = Flask(__name__)
api = Api(app)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        return {"hello": "안녕!"}

if __name__ == "__main__":
    app.run(debug=True, port=5000)