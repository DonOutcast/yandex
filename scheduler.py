# Привет! В общем что смог, то сделал. Остальное даже загуглить не могу.
# По факту просто трачу время, сидя и пялясь в экран. На эту реализацию неделя потрачена))
# Я просто не понимаю даже что гуглить, что бы сделать всё задание.
# Не знаю, может после ревью я с мёртвой точки сдвинусь, поэтому отправляю пока так...
# review
# Привет, не переживай сейчас все найдем ))
from job import Job, get_and_write_data, delete_file, copy_file
from logger import logger
# review
# Я не заметил тут файла logger у тебя, если ты хочешь подключить логирование, то нужно воспользовать logging
# Тут по ссылке можешь пройти для ознакомления https://docs.python.org/3/library/logging.html
import multiprocessing
# review
# Советую посмотреть документацю pep8 по imports https://peps.python.org/pep-0008/#imports
# Также есть такой замечательный инструмент как isort (помогает привести их в порядок)

def coroutine(f):
    def wrap(*args, **kwargs):
        gen = f(*args, **kwargs)
        gen.send(None)
        return gen
    return wrap
# review
# Так у нас с версии python3.5 для работы с corutine есть async/awiat https://docs.python.org/3.5/library/asyncio.html
# Нет необходимости самому реализовывать инициализирующий декоратор плюс код повторяется из файла job.py

class Scheduler(object):
    # review
    # В Python все классы неявно наследуются от базового класса object .
    # Это значит, что даже если при создании класса явно не указывать его родителя,
    # oн все равно будет наследовать от object . Это делается для того,
    # чтобы все классы в Python имели общие базовые атрибуты и методы

    def __init__(
            self,
            max_working_time=1,
            tries=0,
            dependencies=(),
            # review
            # Здесь видать должен быть tuple ?
            # Используй  лучше  функцию tuple() явно
            start_at=None,
    ):
    # review
    # Что у нас с type hint ??
    # Рекомендую ознакомиться с https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
    # Что касается, значения по умолчанию  рекомендую выносить их в константы, чтобы после понимать, на что ограничение
        super().__init__()
    # review
    # Вызов родительского конструктора у object не имеет смысла
        self.task_list: list[Job] = []
        self.start_at = start_at
        self.max_working_time = max_working_time
        self.tries = tries
    # review
    # Type hints
    # Рекомендую ознакомиться с https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
        self.dependencies = dependencies if dependencies is not None else None
    # review
    # Здесь по умолчанию значение tuple, он не будет None даже когда пустой
    # Из этого следует, что условие else никогда не выполнится
    # Если хочешь проверить tuple на пустоту, используй функцию len(dependencies) == 0

    @coroutine
    def schedule(self):
        processes = []
        while True:
            task_list = (yield)
            print(task_list)
            # reivew
            # Видать забыл убрать print() им мы пользуемся только когда что-то проверяем в процессе разработки
            for task in task_list:
                logger.info(f'Планировщик: запускаю задачу - {task.name}')
                p = multiprocessing.Process(target=task.run, args=(condition, url),)
                # Также нужно понимать, что если будут задачи из раздела IO/Bound, то процесс у нас будет поглащен ею
                # Давайка посмотрим статью для начала  https://habr.com/ru/articles/773376/
                p.start()
                processes.append(p)
            for process in processes:
                logger.info(process)
                process.join()
                logger.info(f' process {process} stopped!')
# review
# По поводу корутин и мультипроцессов есть целая книга https://www.manning.com/books/python-concurrency-with-asyncio
# Так что давай остановимся на одном из них

    def run(self, jobs: tuple):
        # review
        # Здесь молодец что указал type hint, но давай дополним tuple[Job]
        gen = self.schedule()
        gen.send(jobs)
# review
# В целом по классу Scheduler нужно реализовать все пункты, которых у нас к сожелению нет
# Давай, повторим материал урока либо свяжемся с метнтором

if __name__ == '__main__':
    condition = multiprocessing.Condition()
    # review
    # (опционально) можно вынести main в отдельный файл
    # Также советую сделать переменную url константной
    url = 'https://official-joke-api.appspot.com/random_joke'
    job1 = Job(
        func=get_and_write_data,
        name='Запрос в сеть',
        args=(condition, url),
    )
    job2 = Job(
        func=copy_file,
        name='Удалить файл',
        args=(condition, ),
    )
    job3 = Job(
        func=delete_file,
        name='Скопировать файл',
        args=(condition,),
    )
    g = Scheduler()
    g.run((job1, job2, job3))
# reivew
# Если ты хочешь запустить это асинхронно, то нужен event.loop
# Давайка, изучим работу с asyncio https://docs.python.org/3/library/asyncio.html