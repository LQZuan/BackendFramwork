import json
from typing import List

from flask import Flask, escape, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@127.0.0.1:3306/lagou4'
db = SQLAlchemy(app)

@app.route('/')
def hello():
    return "hello from ceshiren.com"


class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), unique=True, nullable=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    steps = db.Column(db.String(120), unique=True, nullable=True)

    def __repr__(self):
        return '<TestCase %r>' % self.name


class TestTasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    remark = db.Column(db.String(120), unique=True, nullable=True)

    testcase_id = db.Column(db.Integer, db.ForeignKey('test_case.id'),
                            nullable=False)
    test_case = db.relationship('TestCase',
                               backref=db.backref('test_tasks', lazy=True))

    def __repr__(self):
        return '<TestTasks %r>' % self.name


class TestCaseService(Resource):
    def get(self):
        """
        /testcase.json   /testcase.json?id=1
        :return:
        """
        testcases: List[TestCase] = TestCase.query.all()
        res = [{
            'id': testcase.id,
            'name': testcase.name,
            'description': testcase.description,
            'steps': json.loads(testcase.steps)
        } for testcase in testcases]
        return {
            'body': res
        }

    def post(self):
        """
        /testcase.json  {'name':'xx', 'description': 'xxx', 'steps': []}
        :return:
        """
        testcase = TestCase(
            name=request.json.get('name'),
            description=request.json.get('description'),
            steps=json.dumps(request.json.get('steps'))
        )
        db.session.add(testcase)
        db.session.commit()
        return 'ok'


class TaskService(Resource):
    def post(self):
        print("##########", request.json.get('caseName'))
        testtask = TestTasks(
            name=request.json.get('name'),
            remark=json.dumps(request.json.get('remark')),
            test_case=TestCase(name=request.json.get('caseName'))
        )
        db.session.add(testtask)
        db.session.commit()
        return 'ok'

    def delete(self):
        deltask = TestTasks.query.get(request.data)
        db.session.delete(deltask)
        db.session.commit()
        return 'ok'

    def put(self):
        print(request.json.get('id'))
        updatetask = TestTasks.query.get(request.json.get('id'))
        print("################################", updatetask)
        updatetask.name = request.json.get('name')
        print("################################", updatetask.name)
        db.session.commit()
        return 'ok'

    def get(self):
        testtasks: List[TestTasks] = TestTasks.query.all()
        res = [{
            'id': testtask.id,
            'name': testtask.name,
            'remark': json.loads(testtask.remark),
            'testcase_id': testtask.testcase_id
        } for testtask in testtasks]
        return {
            'body': res
        }


class ReportService(Resource):
    def get(self):
        pass


api.add_resource(TestCaseService, '/testcase')
api.add_resource(TaskService, '/task')
api.add_resource(ReportService, '/report')


if __name__ == '__main__':
    # 启动
    app.run(debug=True)
