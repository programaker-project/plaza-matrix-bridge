import asyncio
import logging
import sys
from plaza_service import (
    PlazaService,
    ServiceConfiguration,
    MessageBasedServiceRegistration,
    ServiceBlock,
    BlockArgument, DynamicBlockArgument,
    BlockType,
)

BOT_ADDRESS = 'plaza@codigoparallevar.com'


class Registerer(MessageBasedServiceRegistration):
    def __init__(self, *args, **kwargs):
        MessageBasedServiceRegistration.__init__(self, *args, **kwargs)

    def get_call_to_action_text(self, extra_data):
        if not extra_data:
            return 'Just greet @plaza-bot:matrix.codigoparallevar.com'.format(bot_addr=BOT_ADDRESS)
        return ('Send the following to @plaza-bot:matrix.codigoparallevar.com<console>!register {user_id}</console>'
                .format(bot_addr=BOT_ADDRESS, user_id=extra_data.user_id))


class MatrixService(PlazaService):
    def __init__(self, bot, storage, *args, **kwargs):
        PlazaService.__init__(self, *args, **kwargs)
        self.storage = storage
        self.SUPPORTED_FUNCTIONS = {
            "get_next_message": self.get_next_message,
            "send_message": self.send_message,
        }
        self.bot = bot
        self.bot.handler = self
        self.message_received_event = asyncio.Event()
        self.registerer = Registerer(self)
        self.rooms = {}
        self.members = {}
        self.bot.start()

    def joined_room(self, room):
        pass

    def set_room_members(self, room, members):
        self.rooms[room] = members
        for member in members:
            if member.user_id not in self.members:
                self.members[member.user_id] = []

            self.members[member.user_id].append(room)

        print(self.members)

    def on_new_message(self, room, event):
        user = event['sender']
        print("R", room)
        print("E", event)
        if not self.storage.is_matrix_user_registered(user):
            self._on_non_registered_event(user, room, event)
        else:
            self.last_message = (room, event)
            self.message_received_event.set()
            self.message_received_event.clear()

    def _on_non_registered_event(self, user, room, event):
        msg = event['content']['body'].strip()
        prefix = '!register '
        if msg.startswith(prefix):
            register_id = msg[len(prefix):]
            self.storage.register_user(user, register_id)
            self.bot.send(room.room_id, "Congrats, you're registered!")

    async def get_next_message(self, extra_data):
        logging.info("Waiting...")
        await self.message_received_event.wait()
        logging.info("New message from {}".format(
            self.last_message[0].display_name))
        return self.last_message[1]['content']['body']

    async def handle_data_callback(self, callback_name, extra_data):
        logging.info("GET {} # {}".format(
            callback_name, extra_data.user_id))
        return {
            "1": {"name": "one"},
            "2": {"name": "two"},
            "3": {"name": "three"},
        }

    async def send_message(self, extra_data, message):
        self.bot.send(message)

    async def handle_call(self, function_name, arguments, extra_data):
        logging.info("{}({}) # {}".format(
            function_name, ", ".join(arguments), extra_data.user_id))
        return await self.SUPPORTED_FUNCTIONS[function_name](extra_data, *arguments)

    def handle_configuration(self):
        return ServiceConfiguration(
            service_name="Matrix",
            is_public=False,
            registration=self.registerer,
            blocks=[
                ServiceBlock(
                    id="get_next_message",
                    function_name="get_next_message",
                    message="Get next Matrix message",
                    arguments=[],
                    block_type=BlockType.GETTER,
                    block_result_type=None,  # TODO: change
                ),
                ServiceBlock(
                    id="send_message",
                    function_name="send_message",
                    message="On channel %1 say %2",
                    arguments=[
                        DynamicBlockArgument(str, "get_available_channels"),
                        BlockArgument(str, "Hello"),
                    ],
                    block_type=BlockType.OPERATION,
                    block_result_type=None,
                ),
            ],
        )
