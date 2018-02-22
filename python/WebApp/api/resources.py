from flask_restful import Resource

class Test(Resource):
    def get(self, var: str):
        return {"status": var}
