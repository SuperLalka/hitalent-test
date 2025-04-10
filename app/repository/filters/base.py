
from sqlalchemy import and_

from app.config.database import Base


class BaseFilter:
    orm_class: Base

    def __init__(self, **fields):
        self.fields = fields

    def __call__(self, base_query, operator=and_):
        print(base_query)
        query = []

        for name, value in self.fields.items():
            if value is None:
                continue

            method_name = f"filter_by_{name}"

            if hasattr(self, method_name):
                method_name = f"filter_by_{name}"
                filter_method = getattr(self, method_name)
                expression = filter_method(value)
                if expression is not None:
                    query.append(expression)

            elif hasattr(self.orm_class, name):
                query.append(getattr(self.orm_class, name) == value)

            print(query)

        print(base_query)

        if not query:
            return base_query

        return base_query.where(operator(*query))
