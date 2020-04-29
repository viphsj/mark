#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by db 20200428 依据示例
from flask import Flask, abort, request, jsonify
from flask_restful import reqparse, abort, Api, Resource
import requests, time, datetime, json

app = Flask(__name__)
api = Api(app)

#转换时间戳
#dateFrom = "2020-4-22"
#dateTo = "2020-4-30"
#转换为毫秒级
#dateFromU = str(int(round(int(time.mktime(time.strptime(dateFrom, "%Y-%m-%d"))) * 1000)))
#dateToU = str(int(round(int(time.mktime(time.strptime(dateTo, "%Y-%m-%d"))) * 1000)))

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '哈哈哈'},
    'todo3': {'task': 'profit!'},
}

CS ={
    "url1": "",
    "head":"",
    "getUrl":""
}

parser = reqparse.RequestParser()
parser.add_argument('task')
parser.add_argument('cookie', type=str)
parser.add_argument('dateFrom', type=str)
parser.add_argument('dateTo', type=str)


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

def dateUtc(dateTime):
    return str(int(round(int(time.mktime(time.strptime(dateTime, "%Y-%m-%d"))) * 1000)))

res = requests.Session()

def getUrl(url):
    res = requests.get(url,headers=CS["head"])
    reportID = json.loads(res.text)
    if len(reportID["data"]) == 5:
        taskID = str(reportID["data"]["result"])
        CS["url1"] = "https://attendance.dingtalk.com/attendance/web/export/downloadLocal/taskProgress.json?taskId=" + taskID
        getUrl(CS["url1"])
    elif len(reportID["data"]) == 2:
        #继续执行 取下载地址
        if reportID["data"]["result"]["progress"] == 100:
            CS["getUrl"] = reportID["data"]["result"]["url"]
        else:
            getUrl(CS["url1"])
    else:
        CS["getUrl"] = "空白"

# # 操作（put / get / delete）单一资源Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# # 操作（post / get）资源列表TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

class get_report_url(Resource):
    def post(self):
        args = parser.parse_args()
        cookies = args['cookie']
        sta = "ok"
        if not cookies:
            cookies = ""
            sta = "false"
        elif len(cookies.strip()) == 0:
            cookies = ""
            sta = "false"
        st = {
            "state":sta,
            "cookie":cookies,
            "from":dateUtc(args['dateFrom']),
            "to":dateUtc(args['dateTo'])
        }
        url = "https://attendance.dingtalk.com/attendance/web/export/downloadLocal/asyncDownload.json?fromTime="+ dateUtc(args['dateFrom']) + "&toTime=" + dateUtc(args['dateTo']) + "&sendMsg=false&deptId=61195601"
        CS["head"] = {"cookie": cookies}
        getUrl(url)

        return jsonify({"downloadUrl": CS["getUrl"]})




# 设置路由
api.add_resource(get_report_url, '/api/get_report_url/v1')
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')

if __name__ == '__main__':
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    app.run(host="0.0.0.0", port=8383, debug=True)
