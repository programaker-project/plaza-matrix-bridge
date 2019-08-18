import traceback
import logging
from matrix_client.client import MatrixClient


class PlazaBot:

    def __init__(self, user, password, instance):
        self.on_message = None
        self.client = MatrixClient(instance)
        self.token = self.client.login(username=user, password=password)
        self.rooms = {}

        self.handler = None
        self.client.add_invite_listener(self.on_invite)

    def start(self):
        for room_id in self.client.get_rooms():
            self.join_room(room_id)

        self.client.start_listener_thread(exception_handler=self.on_exception)

    def send(self, room_id, message):
        self.rooms[room_id].send_text(message)

    def message(self, room, event):
        logging.debug("Room[{}] Event[{}]".format(room, event))
        if self.handler is None:
            return

        try:
            self.handler.on_new_message(room, event)
        except:
            logging.error(traceback.format_exc())

    def on_exception(self, exception):
        logging.error(repr(exception))

    def on_invite(self, room_id, state):
        self.join_room(room_id)

    def join_room(self, room_id):
        room = self.client.join_room(room_id)
        room.add_listener(self.message)
        self.rooms[room_id] = room

        if self.handler is not None:
            self.handler.joined_room(room)
            self.handler.set_room_members(room, room.get_joined_members())
