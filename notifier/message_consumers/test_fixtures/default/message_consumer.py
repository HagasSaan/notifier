messages = input()

print(messages)

with open('/file.txt', 'w') as f:
    f.write(messages)
