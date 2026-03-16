from sqlalchemy import URL

from .enviroment import AvailableDatabases, database_settings


def driver(type: AvailableDatabases) -> str:
    match type:
        case AvailableDatabases.sqlite:
            return "sqlite"
        case AvailableDatabases.mysql:
            return "mysql+pymysql"
        case AvailableDatabases.postgresql:
            return "postgresql+psycopg2"


if database_settings.type == AvailableDatabases.sqlite:
    get_url_database = URL.create(
        drivername=driver(database_settings.type),
        database=database_settings.name_db,
    )
else:
    get_url_database: URL = URL.create(
        drivername=driver(database_settings.type),
        username=database_settings.user,
        password=database_settings.password,
        host=database_settings.host,
        port=database_settings.port,
        database=database_settings.name_db,
    )
