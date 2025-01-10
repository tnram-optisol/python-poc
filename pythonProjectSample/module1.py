import re
import sys

from utils.utils import response_model

pattern = r'^--[a-zA-Z0-9]+'

user_data = sys.argv

my_dict = {}


def parse_data(user_input):
    if len(user_input) > 1:
        for i in range(1, len(user_input)):
            if re.match(pattern, user_input[i]) and user_input[i] != '--help':
                if i + 1 < len(user_input):
                    my_dict[user_input[i].strip().split('--')[1]] = user_input[i + 1]
                continue
    elif user_input == '--help':
        return 'To use this module supply key args in --key args form'
    else:
        return 'Check input or use --help'

    if my_dict:
        return my_dict


if __name__ == "main":
    print(parse_data(user_data))
