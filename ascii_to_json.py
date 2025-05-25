import json
import random as rnd
file_naem = "cat_emotion.json"


# a = """
# /\_/\  
# ( o.o ) 
# > ^ <
# """

# b = """
# /\_/\  
# ( -.- ) 
# > o <
# """

# c = """
# /\_/\  
# ( o.O ) 
# > * <
# """

# d = """
# /\_/\  
# ( >.o ) 
# > ? <
# """



def gen_cats(count: int = 100):
    eye = lambda: rnd.choice(['o', 'O', '>', '<', '*', '-', '∨', '~'])
    item = lambda: rnd.choice(['*', '?', '$', '!'])

    cat = lambda: f"""
/\_/\  
( {eye()}.{eye()} ) 
> {item()} <
"""
    for i in range(count):
        print(cat())


gen_cats()

# data = {
#     "emotion": [
#         f"{a}",
#         f"{b}",
#         f"{c}",
#         f"{d}",
#     ]
# }


# with open(file_naem, 'w') as f:
#     json_data = json.dump(data,f,indent=4)

