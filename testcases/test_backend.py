from datetime import datetime

import requests
from src.backend import db


class TestBackend:
    testcase_url='http://127.0.0.1:5000/testcase'
    testtask_url='http://127.0.0.1:5000/task'

    # 按照数据结构设计，创建数据表
    def setup(self):
        db.create_all()

    # 添加测试用例
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

    # 获取测试用例列表
    def test_testcase_get(self):
        r=requests.get(self.testcase_url)
        assert r.json()['body']
        print(r.json()['body'])

    # 添加测试任务
    def test_testtask_post(self):
        r = requests.post(
            self.testtask_url,
            json={
                'name': f'task1 {datetime.now().isoformat()}',
                'remark': ['1', '2', '3'],
                'caseName': f'Case {datetime.now().isoformat()}'
            }
        )

        assert r.status_code == 200

    # 获取测试任务
    def test_testtask_get(self):
        r=requests.get(self.testtask_url)
        assert r.json()['body']
        print(r.json()['body'])

    # 删除测试任务
    def test_deltask(self):
        r=requests.delete(self.testtask_url, data='1')
        assert r.status_code == 200

    # 更新、修改测试任务
    def test_updatetask(self):
        r = requests.put(
            self.testtask_url,
            json={
                'id': '2',
                'name': f'task1 {datetime.now().isoformat()}'
            }
        )
        assert r.status_code == 200