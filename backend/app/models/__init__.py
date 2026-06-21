from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.models.profile import Profile  # noqa: E402, F401
from app.models.item import Item  # noqa: E402, F401
from app.models.run import Run, RunItem  # noqa: E402, F401
