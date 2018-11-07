import asyncio

from asgiref.server import StatelessServer


class BeatServer(StatelessServer):
    def __init__(self, application, channel_layer, beat_config, max_applications=1000):
        super().__init__(application, max_applications)
        self.channel_layer = channel_layer
        if self.channel_layer is None:
            raise ValueError("Channel layer is not valid")
        self.beat_config = beat_config

    async def application_send(self, scope, message):
        pass

    async def handle(self):
        """
        Listens on all the provided channels and handles the messages.
        """
        # For each channel, launch its own listening coroutine
        listeners = []
        for each in self.beat_config:
            listeners.append(asyncio.ensure_future(
                self.listener(each['channel'])
            ))

        # For each beat configuration, launch it's own sending pattern
        emitters = []
        for each in self.beat_config:
            emitters.append(asyncio.ensure_future(
                self.emitters(each)
            ))

        # Wait for them all to exit
        await asyncio.wait(emitters)
        await asyncio.wait(listeners)

    async def emitters(self, config):
        """
        Single-channel emitter
        """
        while True:
            await asyncio.sleep(config['schedule'].total_seconds())

            await self.channel_layer.send(config['channel'], {
                "type": config['type'],
                "message": config['message']
            })

    async def listener(self, channel):
        """
        Single-channel listener
        """
        while True:
            message = await self.channel_layer.receive(channel)
            if not message.get("type", None):
                raise ValueError("Worker received message with no type.")
            # Make a scope and get an application instance for it
            scope = {"type": "channel", "channel": channel}
            instance_queue = self.get_or_create_application_instance(channel, scope)
            # Run the message into the app
            await instance_queue.put(message)
