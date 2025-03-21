import os
import datetime
from pathlib import Path
import pandas as pd
import requests
from dotenv import load_dotenv


#Импорт ключ from src.

#Загрузка переменных окружения
load_dotenv()
api_key = os.getenv("API_KEY")

#определение текущего каталога
current_dir = Path(__file__).parent.parent.resolve()
dir_transactions_excel = current_dir/'data'/'operations.xlsx'

def day_time_now():
    """Функция приветствия"""

    current_date_time = datetime.datetime.now()
    hour = current_date_time.hour

    if 0 <= hour < 6 or 22 <= hour <= 23:
        return "Доброй ночи"
    elif 17 <= hour <= 22:
        return "Добрый вечер"
    elif 7 <= hour <= 11:
        return "Доброе утро"
    else:
        return "Добрый день"

def user_transactions(data_time: pd.Timestamp) -> pd.DataFrame:
    """Функция извлечения"""

    df = pd.read_excel(dir_transactions_excel)
    df_filtered = df.loc[(pd.to_datetime(df['Дата операции'],dayfirst=True) <= data_time) &
            (pd.to_datetime(df['Дата операции'], dayfirst=True) >= data_time.replace(day=1))].copy()

    df_filtered.loc[:, 'кэшбек'] = df_filtered['Сумма операции с округлением'] // 100
    sales_by_card = df_filtered.groupby('Номер карты')[['Сумма операции с округлением', 'кэшбек']].sum()
    sorted_sales = sales_by_card.sort_values(by='Сумма операции с округлением', ascending=False)

    return sorted_sales

def max_five_transactions(data_time: pd.Timestamp) -> pd.DataFrame:
    """
    Функция, которая извлекает 5 лучших транзакций по сумме платежа.
    """
    df = pd.read_excel(dir_transactions_excel)

    filtered_df = df.copy()

    # Фильтрация транзакций за указанный месяц
    filtered_df = filtered_df.loc[
        (pd.to_datetime(filtered_df['Дата операции'],
                        format="%d.%m.%Y %H:%M:%S", dayfirst=True) <= data_time) &
        (pd.to_datetime(filtered_df['Дата операции'],
                        format="%d.%m.%Y %H:%M:%S", dayfirst=True) >= data_time.replace(day=1))
        ]

    # Сортировка и получение 5 лучших транзакций
    top_transactions = filtered_df.sort_values(by='Сумма операции с округлением', ascending=False).head(5)
    return top_transactions


#def exchange_rate() -> list:
    """
    Функция, которая извлекает курсы обмена для USD и EUR к RUB
    путем вызова внешнего API.
    """


    # for currency in currency_list:
    #     url = f"https://api.apilayer.com/currency_data/convert"
    #     headers = {"apikey": api_key,
    #                "to":"RUB",
    #                "from":"currency",
    #                "amount":"1"
    #     }

def exchange_rate() -> list:

    currency_list = ["USD", "EUR"]
    convert_to = "RUB"
    new_currency_list = []
    for currency in currency_list:

        #url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount={amount}"


        url = f"https://api.apilayer.com/exchangerates_data/convert?to={convert_to}&from={currency}&amount=1"
        headers = {"apikey": api_key}
        response = requests.get(url, headers=headers)
        result = response.json()
        currency_value = result.get('result')

        if currency_value is not None:
            new_currency_list.append(currency_value)
        else:
            print("Ошибка: ключ 'result' не найден в ответе для:", currency)

    return new_currency_list

print(exchange_rate())