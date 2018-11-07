from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from django.conf.urls import url

import ws.consumers

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            url(r'^ws/(?P<room_name>[^/]+)/$', ws.consumers.ChatConsumer),
        ])
    ),
    "channel": ChannelNameRouter({
        "ws": ws.consumers.ChatConsumer,
        "data_push": ws.consumers.DataServer
    }),
})
