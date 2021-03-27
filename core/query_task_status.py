from __future__ import absolute_import
import json, time

from channels.generic.websocket import WebsocketConsumer

from whole_process_test.views import QueryInstanceInfo


class QueryStatusConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def websocket_receive(self, message):
        print('message--', message)
        instance_id = message['text']
        print('instance_id--', instance_id)

        while True:
            info = QueryInstanceInfo(instance_id).get_instance_info()
            self.send(text_data=json.dumps({
                'message': info
            }))
            if info.get('test_status', '') == '测试完成':
                break
            else:
                time.sleep(10)

    def send_message(self, event):
        self.send(text_data=json.dumps({
            "message": event["message"]
        }))

