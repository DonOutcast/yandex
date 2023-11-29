import shutil
from urllib.request import urlopen
from pathlib import Path
import ssl
import json
# review
# Советую посмотреть документацю pep8 по imports https://peps.python.org/pep-0008/#imports
# Также есть такой замечательный инструмент как isort (помогает привести их в порядок)
from logger import logger
# review
# Я не заметил тут файла logger у тебя, если ты хочешь подключить логирование, то нужно использовать logging
# Тут по ссылке можешь пройти для ознакомления https://docs.python.org/3/library/logging.html

def coroutine(f):
    def wrap(*args, **kwargs):
        gen = f(*args, **kwargs)
        gen.send(None)
        return gen
    return wrap
# review
# Так, у нас с версии python3.5 для работы с corutine есть async/awiat https://docs.python.org/3.5/library/asyncio.html
# Нет необходимости самому реализовывать инициализирующий декоратор, плюс код повторяется из файла scheduler.py


def get_and_write_data(condition, url):
    # review
    # Type hints
    # Рекомендую ознакомиться с https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
    # Среди разработчиков есть некий кодекс кода и он гласит, что функция должна делать только одну вещь и делать ее хорошо
    # Давай, декомпозируем это на две функции
    context = ssl._create_unverified_context()
    file = 'punchline.txt'
    # review
    # А давай, мы будем передавать путь до файла в аргументах, у нас же не только этот файл будет
    with condition:
        with urlopen(url, context=context) as req:
    # review
    # Рекомендую использовать aiohtpp или requests так как urlopen() совсем уж древний
    #  https://habr.com/ru/companies/kts/articles/560058/
    # https://pypi.org/project/requests/
            resp = req.read().decode("utf-8")
            resp = json.loads(resp)
        if req.status != 200:
            raise Exception(
                "Error during execute request. {}: {}".format(
                    resp.status, resp.reason
                )
            )
        # review
        # Сюда бы добaвить логгирования, чтобы мы понимали, где был raise
        data = resp
        if isinstance(data, dict):
            path = Path(file)
            setup = data['setup']
            punchline = data['punchline']
            # review
            # Используй get, так ты обезапосишь себя от  исключения  KeyError
            print(
                f'Setup: {setup} \n'
                f'Punchline: {punchline}'
            )
            # reivew
            # Видать забыл убрать print() им мы пользуемся только когда что-то проверяем в процессе разработки
            with open(path, mode='a') as config:
                config.write(str(data))
        else:
            logger.error(type(data))
            logger.error(ValueError)
            raise ValueError


def copy_file(condition, x=None):
    file = 'punchline.txt'
    to_path = './jokes/'
    with condition:
        condition.wait(timeout=1)
# review
# Представим ситуацию, что один поток не успел поработать с файлом за выделенную ему секунду, и что тогда ?
# Будет состояние гонки, а за этим следует много чего интерестного,  давай изучим, как с этим бороться https://habr.com/ru/companies/simbirsoft/articles/701020/
        try:
            shutil.copy(file, to_path)
        except FileNotFoundError as ex:
            logger.error('Файл не найден %s', ex)


def delete_file(condition, x=None):
# review
# Название перменной должно отображать ее суть, тут не совсем понятно, что такое х и зачем он в коде, он не используется
# Рекомендую посмотреть такой линтер как ruff, его можно настроить, чтобы удалял из кода неиспользуемые перменные https://docs.astral.sh/ruff/
    file = 'punchline.txt'
    # review
    # А давай, мы будем передавать путь до файла в аргументах, у нас же не только этот файл будет
    obj = Path(file)
    with condition:
        condition.wait(timeout=1)
        try:
            obj.unlink()
            logger.info('Удалил файл')
        except FileNotFoundError as ex:
            logger.error(ex)


class Job:
    def __init__(
            self,
            func=None,
            name=None,
            args=None,
    ):
    # reivew
    # По условию нам нужно, чтобы у задачи был некий timeout необязательный аргумент
    # Также время запуска statrt_at и count_of_retry по умолчанию равный 0
    # пропустил еще зависимости dependence
        self.args = args
        self.name = name
        self.func = func

    def run(self, *args):
        tar = self.func(*args)
        logger.info('тип объекта в Job.run %s', type(tar))
        logger.debug('запуск объекта %s', tar)
        # review
        # А здесь нам нужно будет с тобой прописать конфигурацию для уровний логирования, иначе это так работать не будет
        # Советую ознакомиться с уровнями логирования https://habr.com/ru/companies/wunderfund/articles/683880/
        return tar
