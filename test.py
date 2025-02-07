import json
line = ["tim", "jim", "bob"]
array = json.dumps(line)

print(array)
print(type(array))
print(type(line))

line2 = json.loads(array)

print(line2)
print(type(line2))