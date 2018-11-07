import channels.layers
from asgiref.sync import async_to_sync

if __name__ == '__main__':
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)('chat_home', {'type': 'chat_message_with_end', 'message': 'hello'})
