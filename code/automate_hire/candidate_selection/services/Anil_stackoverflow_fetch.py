import requests
from database.util import add_user_data_from_se
from data_cleaning_stackoverlow import get_stack_exchange_data


def get_user_data(page_number):
    url = f'https://api.stackexchange.com/2.3/users?page={page_number}&pagesize=100&order=desc&sort=reputation&site' \
          f'=stackoverflow'

    user_data = requests.get(url).json()

    return user_data


def fetch_data_from_api():

    profile_length = (len(get_stack_exchange_data()) // 100) + 1

    for i in range(profile_length, profile_length + 5):
        try:
            json_data = get_user_data(i)

            # for item in json_data['items']:
            #     add_user_data_from_se(item)
        except Exception as e:
            print(e)


if _name_ == '_main_':
    fetch_data_from_api()