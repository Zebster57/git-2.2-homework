import os
import sqlalchemy as sq

from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from Test.db.models import create_tables, Items, Resource


"""
Для корректной работы этого модуля:
Необходимо добавить файл .env в каталог \db\ со следующими параметрами:

USER_="имя пользователя PostgreSQL"
PASSWORD="пароль пользователя PostgreSQL"
HOST="хост"
PORT=порт
"""

load_dotenv()

USER = os.getenv('USER_')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

name_db = 'parse_kz'
DSN = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{name_db}'


class FuncDB():
    """Класс для взаимодействия с базой данных parse_kz с помощью библиотеки SQLalchemy"""

    def __init__(self):
        """
        При создании экземпляра класса, создается БД, таблицы в ней и открывается сессия для работы с ней.
        engine:  Функция sqlalchemy.create_engine() создает новый экземпляр класса sqlalchemy.engine.
                 Engine который предоставляет подключение к базе данных.
        create_database: Создание БД
        create_tables: Создание таблиц в БД
        session: экземпляр класса sqlalchemy.orm sessionmaker создает подключение к текущей БД
        """
        engine = sq.create_engine(DSN)

        if not database_exists(engine.url):
            create_database(engine.url)
            create_tables(engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add_new_resource(self, link: str, title: str,
                         top_tag,
                         bottom_tag,
                         title_cut,
                         date_cut) -> bool:
        """
        Метод класса позволяет добавить данные о новом новостном ресурсе в таблицу Resource
        :params link: str - ссылка не ресурс
        :params title: str - название ресурса

        :return: bool True
        """

        new_resource = Resource(
            RESOURCE_NAME=title,
            RESOURCE_URL=link,
            top_tag=top_tag,
            bottom_tag=bottom_tag,
            title_cut=title_cut,
            date_cut=date_cut
        )

        self.session.add(new_resource)
        self.session.commit()

        return True

    def get_resource(self, *args):
        for resource_id in args:
            query = self.session.query(Resource).filter(Resource.RESOURCE_ID == resource_id).all()
            if query:

                return {
                    'url': query[0].RESOURCE_URL,
                    'top_tag': query[0].top_tag,
                    'bottom_tag': query[0].bottom_tag,
                    'date_cut': query[0].date_cut,
                    'title_cut': query[0].title_cut
                }

    def get_id_resource(self, title: str) -> int:
        """
        Метод класса позволяет получить Recource.RESOURCE_ID по названию ресурса
        :params title: str - название ресурса

        :return: int - Если данный RESOURCE_ID обнаружен в БД
                 None - Если данный RESOURCE_ID не обнаружен в БД
        """

        query = self.session.query(Resource).filter(Resource.RESOURCE_NAME == title).all()
        if query:

            return query[0].RESOURCE_ID

    def add_new_news(self, resource_id: str, link: str, title: str, content: str, nd_date, not_date) -> bool:
        """
        Метод класса позволяет добавить данные конкретной статьи
        :params resource_id: str - ID ресурса из таблицы Resource
        :params link: str - ссылка не новость
        :params title: str - название новости
        :params content: str - текст новости
        :params nd_date: int - дата публикации новости в формате Unixtime
        :params not_date: str - дата публикации новости в формате "YYYY-MM-DD"

        :return: bool True
        """

        new_item = Items(
            res_id=resource_id,
            link=link,
            title=title,
            content=content,
            nd_date=nd_date,
            not_date=not_date
        )

        self.session.add(new_item)
        self.session.commit()

        return True

    def news_in_db(self, res_id: int, url: str) -> bool:
        """
        Метод класса позволяет проверить существует ли данные об этой новости по ссылке
        :params res_id: int - ID ресурса из БД
        :params url: str - ссылка на новость

        :return: bool - True если данный url найдет в таблице Items
                        False если данный url не найден в таблице Items
        """

        q = self.session.query(Items).join(Resource).filter(Resource.RESOURCE_ID == res_id).filter(Items.link == url) \
            .all()

        if q:
            return True
        return False

    def resource_in_db(self, url: str) -> bool:
        """
        Метод класса позволяет проверить существует ли данные об этом ресурсе по его названию
        :params title: str - название ресурса

        :return: bool - True если данный title найдет в таблице Resource
                        False если данный title не найден в таблице Resource
        """

        q = self.session.query(Resource).filter(Resource.RESOURCE_URL == url).all()

        if q:
            return True
        return False

    def close(self) -> None:
        """
        Метод для закрытия текущей сессии

        :return: None
        """
        self.session.close()
        
def add_data(data: list, *models):
    for model in models:
        string = str(model).lower()
        model_str = string[25:].strip("'>")
        for dictionary in data:
            if dictionary['model'] == model_str:
                session.add(model(id=dictionary.get('pk'), **dictionary.get('fields')))
            session.commit()


def output_publisher(pers_input):
    if pers_input.isdigit():
        query = session.query(Publisher).filter(Publisher.id == pers_input).all()
    else:
        query = session.query(Publisher).filter(Publisher.name == pers_input).all()
    if query:
        for output in query:
            return output
    return 'Publisher with this id does not exist'


def output_shop(pers_input):
    query = session.query(Shop)
    query = query.join(Stock)
    query = query.join(Book)
    query = query.join(Publisher)
    if pers_input.isdigit():
        query = query.filter(Publisher.id == pers_input).all()
    else:
        query = query.filter(Publisher.name == pers_input).all()
    if query:
        for output in query:
            return output
    return 'Publisher with this id does not exist'


if __name__ == "__main__":
    pass













