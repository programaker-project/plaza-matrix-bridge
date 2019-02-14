import logging
from matrix_client.client import MatrixClient


class PlazaBot:

    def __init__(self, user, password, instance):
        self.on_message = None
        self.client = MatrixClient(instance)
        self.token = self.client.login(username=user, password=password)

        self.client.add_invite_listener(self.on_invite)
        for room_id in self.client.get_rooms():
            room = self.client.join_room(room_id)
            room.add_listener(self.message)
        self.client.start_listener_thread(exception_handler=self.on_exception)

    def message(self, room, event):
        logging.info("Room[{}] Event[{}]".format(room, event))
        if self.on_new_message is None:
            return

        self.on_new_message(room, event)

    def on_exception(self, exception):
        logging.error(repr(exception))

    def on_invite(self, room_id, state):
        room = self.client.join_room(room_id)
        room.add_listener(self.message)
