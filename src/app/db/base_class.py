from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str
    # the subclass could generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

if __name__ == '__main__':
    from app.db.session import engine
    # 创建数据表前必须先导入继承 Base 的类
    from app.models.user import *
    Base.metadata.create_all(engine)
