nested_dict = \
    {
        "variables":
            {
                "x": 10,
                "y": 20,
                "z": 30
            },
        "person2":
            {
                "name": "Bob",
                "age": 25
            }
    }

variables = None

x = '10'

print(eval(x, variables))