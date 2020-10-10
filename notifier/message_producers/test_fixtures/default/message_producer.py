import json

messages = [
    {
        'sender': 'user1',
        'receiver': 'user2',
        'content': 'content1',
    },
    {
        'sender': 'user2',
        'receiver': 'user1',
        'content': 'content2',
    },
]

print(json.dumps(messages))
