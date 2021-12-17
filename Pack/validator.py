import json
import re
from tqdm import tqdm


class File:
    def __init__(self, path: str) -> None:
        self._data = json.load(open(path, encoding='utf-8'))

    @property
    def data(self) -> list:
        return self._data


class Validator:
    _telephone: str
    _weight: float
    _inn: str
    _passport_number: str
    _university: str
    _work_experience: float
    _political_views: str
    _worldview: str
    _address: str
    _invalid_university: list = ['Каражан',
                                 'Бан Ард',
                                 'Аретуза',
                                 'Гвейсон Хайль',
                                 'Хогвартс',
                                 'Кирин-Тор',
                                 'Шармбатон',
                                 'Дурмстранг']
    _valid_political_views: list = ['Индифферентные',
                                    'Социалистические',
                                    'Консервативные',
                                    'Коммунистические',
                                    'Либеральные',
                                    'Умеренные',
                                    'Анархистские',
                                    'Либертарианские']
    _valid_worldview: list = ['Пантеизм',
                              'Секулярный гуманизм',
                              'Деизм',
                              'Атеизм',
                              'Иудаизм',
                              'Католицизм',
                              'Конфуцианство',
                              'Агностицизм',
                              'Буддизм']

    def __init__(self, data: dict):
        """
        Инициализируется объект класса Validator
        :param data: dict
        Передается словарь со всеми полями данных
        """
        self._telephone = data['telephone']
        self._weight = data['weight']
        self._inn = data['inn']
        self._passport_number = data['passport_number']
        self._university = data['university']
        self._work_experience = data['work_experience']
        self._political_views = data['political_views']
        self._worldview = data['worldview']
        self._address = data['address']

    def check_telephone(self) -> bool:
        """
        Проверяет номер телефона на валидность.
        """
        if re.match(r"(?:\+7|8)-\(\d{3}\)(-\d{3})(-\d{2}){2}", self._telephone) is not None:
            return True
        return False

    def check_weight(self) -> bool:
        """
        Проверяет значение веса на валидность.
        """
        if (re.match(r"^\d{2,3}$", str(self._weight)) is not None) and (int(float(self._weight) < 2000)) and \
                int((float(self._weight)) > 30):
            return True
        return False

    def check_inn(self) -> bool:
        """
        Проверяет номер ИНН на валидность.
        """
        if re.match(r"^\d{12}$", self._inn) is not None:
            return True
        return False

    def check_passport_number(self) -> bool:
        """
        Проверяет номер паспорта на валидность.
        """
        if re.match(r"^\d{6}$", str(self._passport_number)) is not None:
            return True
        return False

    def check_university(self) -> bool:
        """
       Проверяет название университета на валидность.
        """
        if (re.match(r"^([А-яA-z]+\.?\s?-?)+$", self._university) is not None) and \
                (self._university not in self._invalid_university):
            return True
        return False

    def check_work_experience(self) -> bool:
        """
        Проверяет значение опыта работы на валидность.
        """
        if (re.match(r"^\d+$", str(self._work_experience)) is not None) and (
                int(float(self._work_experience)) > 0) and (int(float(self._work_experience)) < 60):
            return True
        return False

    def check_political_views(self) -> bool:
        """
        Проверяет политические взгляды на валидность.
        """
        if (re.match(r"^(([А-яA-z])+\.?\s?-?)+$", self._political_views) is not None) and \
                (self._political_views in self._valid_political_views):
            return True
        return False

    def check_worldview(self) -> bool:
        """
        Проверяет взгляд на мир на валидность.
        """
        if (re.match(r"^([А-яA-z]+\.?\s?-?)+$", self._worldview) is not None) and \
                (self._worldview in self._valid_worldview):
            return True
        return False

    def check_address(self) -> bool:
        """
        Проверяет адрес на валидность.
        """
        if re.match(r"^[A-я.]+\s[\w .()-]+\d+$", self._address) is not None:
            return True
        return False

    def check_data(self) -> list:
        """
        Проверяет все поля на валидность
        Если в каком-либо поле найдена ошибка, то оно записывается в список
        Возвращает список с данными пользователя, у которого присутствует невалидная запись
        """
        invalid_values = []
        if not self.check_telephone():
            invalid_values.append("telephone")
        if not self.check_weight():
            invalid_values.append("weight")
        if not self.check_inn():
            invalid_values.append("inn")
        if not self.check_passport_number():
            invalid_values.append("passport_number")
        if not self.check_university():
            invalid_values.append("university")
        if not self.check_work_experience():
            invalid_values.append("work_experience")
        if not self.check_political_views():
            invalid_values.append("political_views")
        if not self.check_worldview():
            invalid_values.append("worldview")
        if not self.check_address():
            invalid_values.append("address")
        return invalid_values


def file_validate(file_input: str, file_output: str):
    data = File(file_input).data
    count_valid = 0
    count_invalid = 0
    dict_invalid_records = {"telephone": 1000,
                            "weight": 1000,
                            "inn": 1000,
                            "passport_number": 1000,
                            "university": 1000,
                            "work_experience": 1000,
                            "political_views": 1000,
                            "worldview": 1000,
                            "address": 1000}
    list_result = []

    with tqdm(data, desc="Прогресс обработки записей") as progressbar:
        for elem in data:
            check = Validator(elem).check_data()
            if len(check) == 0:
                count_valid += 1
                list_result.append(
                    {
                        "telephone": elem["telephone"],
                        "weight": elem["weight"],
                        "inn": elem["inn"],
                        "passport_number": elem["passport_number"],
                        "university": elem["university"],
                        "work_experience": elem["work_experience"],
                        "political_views": elem["political_views"],
                        "worldview": elem["worldview"],
                        "address": elem["address"]
                    }
                )
            else:
                count_invalid += 1
            progressbar.update(1)

    with open(file_output, 'w', encoding='utf-8') as output:
        json.dump(list_result, output, indent=4, ensure_ascii=False)

    print(f"Count of valid records: {count_valid}")
    print(f"Count of invalid records: {count_invalid}")
    print("Count of invalid entries by type of error:")
    for key, value in dict_invalid_records.items():
        print(" " * 4 + str(key) + ": " + str(value))


