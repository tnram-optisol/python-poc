import  random

def generate_account_number():
    account_number = ''
    for i in range(2, 12):
        if i == 0:
            continue
        else:
            account_number = account_number + str(random.randint(2, i))
    return {'account_number': account_number}

def convert_rows_to_dict(rows):
    result = [dict(row) for row in rows]
    return  result