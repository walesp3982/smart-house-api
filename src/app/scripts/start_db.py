from app.models import engine, metadata


def create_tables():
    metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()
