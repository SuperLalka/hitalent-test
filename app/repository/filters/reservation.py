
from app.models import Reservation
from app.repository.filters.base import BaseFilter


class ReservationFilter(BaseFilter):
    orm_class = Reservation

    def filter_by_list_id(self, value):
        return self.orm_class.id.in_(value)

    def filter_by_customer_name(self, value):
        return self.orm_class.customer_name == value

    def filter_by_reservation_time(self, value):
        return self.orm_class.reservation_time == value

    def filter_by_reservation_time_end(self, value):
        return self.orm_class.reservation_time_end == value

    def filter_by_table_id(self, value):
        return self.orm_class.table_id == value
