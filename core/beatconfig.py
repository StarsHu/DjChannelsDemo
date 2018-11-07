from datetime import timedelta

BEAT_SCHEDULE = [
    {
        'channel': 'data_push',
        'schedule': timedelta(seconds=5),
        'type': 'summary',
        'message': {'foo': 'bar'},
    },
]
