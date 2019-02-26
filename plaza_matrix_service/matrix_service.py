import asyncio
import logging
import sys
from plaza_service import (
    PlazaService,
    ServiceConfiguration,
    MessageBasedServiceRegistration,
    ServiceBlock,
    BlockArgument,
    BlockType,
)

from plaza_gitlab_service import serializers

BOT_ADDRESS = 'plaza@codigoparallevar.com'


class Registerer(MessageBasedServiceRegistration):
    def __init__(self, *args, **kwargs):
        MessageBasedServiceRegistration.__init__(self, *args, **kwargs)

    def get_call_to_action_text(self):
        return '''Just greet <u>@plaza-bot:matrix.codigoparallevar.com</u>'''.format(bot_addr=BOT_ADDRESS)


class MatrixService(PlazaService):
    def __init__(self, bot, *args, **kwargs):
        PlazaService.__init__(self, *args, **kwargs)
        self.SUPPORTED_FUNCTIONS = {
            "get_next_message": self.get_next_message,
            "send_message": self.send_message,
        }
        self.bot = bot
        self.bot.on_new_message = self.on_new_message
        self.message_received_event = asyncio.Event()
        self.registerer = Registerer(self)

    def on_new_message(self, room, event):
        self.last_message = (room, event)
        self.message_received_event.set()
        self.message_received_event.clear()

    async def get_next_message(self, extra_data):
        logging.info("Waiting...")
        await self.message_received_event.wait()
        logging.info("New message from {}".format(
            self.last_message[0].display_name))
        return self.last_message[1]['content']['body']

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
                    message="Send Matrix message: %1",
                    arguments=[BlockArgument(str, "Hello")],
                    block_type=BlockType.OPERATION,
                    block_result_type=None,
                ),
            ],
        )
