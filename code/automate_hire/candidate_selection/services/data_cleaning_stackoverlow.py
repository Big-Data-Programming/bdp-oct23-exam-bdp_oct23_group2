import re
import pandas as pd
from datetime import datetime, timedelta
from database.connector import get_sql_engine

DATA_FETCHED_DATE = datetime.fromtimestamp(1674604800)


def value_to_float(value):
    try:
        value = float(value)
    except ValueError:
        pass

    if type(value) == float:
        return value

    if 'k' in value:
        if len(value) > 1:
            return float(value.replace('k', '')) * 1000

    if 'm' in value:
        if len(value) > 1:
            return float(value.replace('m', '')) * 1000000

    return 0


def remove_comma(value):

    if value == "":
        return 0
    elif "," in value:
        return int(value.replace(",", ""))
    else:
        return int(value)


def join_date_string_to_date(value):
    years = 0
    if 'years' in value:
        match = re.match(r'(\d+) years.*', value)
        years = int(match.group(1))
    elif 'year' in value:
        years = 1

    months = 0
    if 'months' in value:
        match = re.match(r'.(\d+) months.', value)
        months = int(match.group(1))
    elif 'month' in value:
        months = 1

    joined_date = DATA_FETCHED_DATE - timedelta(days=((years * 365) + (months * 30)))

    return int(joined_date.timestamp())


def last_online_string_to_date(value):
    last_online_date = 0

    if 'years' in value:
        match = re.match(r'.(\d+) years.', value)
        years = int(match.group(1))
        last_online_date = DATA_FETCHED_DATE - timedelta(days=(years * 365))
    elif 'year' in value:
        last_online_date = DATA_FETCHED_DATE - timedelta(days=365)

    if 'month' in value:
        last_online_date = DATA_FETCHED_DATE - timedelta(days=30)

    if 'week' in value:
        last_online_date = DATA_FETCHED_DATE - timedelta(days=7)

    try:
        return int(last_online_date.timestamp())
    except AttributeError:
        return int(DATA_FETCHED_DATE.timestamp())


def get_refined_user_data():
    engine = get_sql_engine()
    dataframe = pd.read_sql("user_raw_data", con=engine)

    dataframe['reached'] = dataframe['reached'].apply(value_to_float)

    dataframe['reputation'] = dataframe['reputation'].apply(remove_comma)
    dataframe['answers'] = dataframe['answers'].apply(remove_comma)
    dataframe['questions'] = dataframe['questions'].apply(remove_comma)
    dataframe['goldbadges'] = dataframe['goldbadges'].apply(remove_comma)
    dataframe['silverbadges'] = dataframe['silverbadges'].apply(remove_comma)
    dataframe['bronzebadges'] = dataframe['bronzebadges'].apply(remove_comma)

    dataframe['joindate'] = dataframe['joindate'].apply(join_date_string_to_date)
    dataframe['lastonline'] = dataframe['lastonline'].apply(last_online_string_to_date)

    return dataframe


def get_stack_exchange_data():
    engine = get_sql_engine()
    return pd.read_sql("stackexchange_users", con=engine)


if _name_ == '_main_':
    df = get_refined_user_data()
    print(df.info())

    df = get_stack_exchange_data()
    print(df.info())