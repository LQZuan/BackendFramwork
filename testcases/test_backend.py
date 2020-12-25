from datetime import datetime

import requests
from src.backend import db


class TestBackend:
    testcase_url='http://127.0.0.1:5000/testcase'
    testtask_url='http://127.0.0.1:5000/task'


    def test_testcase_post(self):
        r=requests.post(
            self.testcase_url,
            json={
                'name': f'case1 {datetime.now().isoformat()}',
                'description': 'description1',
                'steps': ['1', '2', '3']
            }
        )

        assert r.status_code == 200

    def test_testcase_get(self):
        r=requests.get(self.testcase_url)
        assert r.json()['body']
        print(r.json()['body'])

    def test_create_table(self):
        db.create_all()

    def test_testtask_post(self):
        r = requests.post(
            self.testtask_url,
            json={
                'caseId': '1',
                'name': f'task1 {datetime.now().isoformat()}',
                'remark': ['1', '2', '3']
            }
        )

        assert r.status_code == 200

    def test_testtask_get(self):
        r=requests.get(self.testtask_url)
        assert r.json()['body']
        print(r.json()['body'])

    def test_deltask(self):
        r=requests.delete(self.testtask_url, data='1')
        assert r.status_code == 200

    def test_updatetask(self):
        r = requests.put(
            self.testtask_url,
            json={
                'caseId': '1',
                'name': f'task1 {datetime.now().isoformat()}'
            }
        )
        assert r.status_code == 200