import datetime
import psycopg2 as ps
import datetime
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, select, and_
from sqlalchemy.orm import relationship
from db import Orders, Session, engine


def recreate_database():
    Orders.metadata.drop_all(engine)
    Orders.metadata.create_all(engine)


class Order(Orders):
    __tablename__ = 'Orders'
    order_id = Column(Integer, primary_key=True)
    order_date = Column(Date)
    customer_id = Column(Integer, ForeignKey('Customers.customer_id'))
    car_id = Column(Integer, ForeignKey('Cars.car_id'))
    stuff_id = Column(Integer, ForeignKey('Stuff.stuff_id'))
    #customer = relationship("Customers")
    #car = relationship("Cars")
    #stuff = relationship("Stuff")

    def __init__(self, order_id, order_date,customer_id,car_id,stuff_id):
        self.order_id = order_id
        self.order_date = order_date
        self.car_id = car_id
        self.customer = customer_id
        self.stuff_id = stuff_id

    def __repr__(self):
        return "{:>10}{:>10}{:>15}{:>10}\t\t{}" \
            .format(self.order_id, self.customer_id , self.car_id, self.stuff_id, self.order_date)


class Customer(Orders):
    __tablename__ = 'Customers'
    customer_id = Column(Integer, primary_key=True)
    customer_name = Column(String)
    customer_surname = Column(String)
    customer_telephone = Column(String)

    def __init__(self, customer_id, customer_name, customer_surname, customer_telephone):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.customer_surname = customer_surname
        self.customer_telephone = customer_telephone

    def __repr__(self):
        return "{:>10}{:>15}{:>25}{:>45}" \
            .format(self.customer_id, self.customer_name, self.customer_surname, self.customer_telephone)


class Car(Orders):
    __tablename__ = 'Cars'
    car_id = Column(Integer, primary_key=True)
    brand_name = Column(String)
    model_name = Column(String)
    year_of_manufacture = Column(String)

    def __init__(self, car_id, brand_name, model_name, year_of_manufacture):
        self.car_id = car_id
        self.brand_name = brand_name
        self.model_name = model_name
        self.year_of_manufacture = year_of_manufacture

    def __repr__(self):
        return "{:>10}{:>55}{:>65}{:>10}" \
            .format(self.car_id, self.brand_name, self.model_name, self.year_of_manufacture)


class Stuff(Orders):
    __tablename__ = 'Stuff'
    stuff_id = Column(Integer, primary_key=True)
    stuff_surname = Column(String)
    stuff_telephone = Column(String)
    date_start_working = Column(String)

    def __init__(self, stuff_id, stuff_surname, stuff_telephone, date_start_working):
        self.stuff_id = stuff_id
        self.stuff_surname = stuff_surname
        self.stuff_telephone = stuff_telephone
        self.date_start_working = date_start_working

    def __repr__(self):
        return "{:>10}{:>25}{:>45}{:>35}" \
            .format(self.stuff_id, self.stuff_surname, self.stuff_telephone, self.date_start_working)

class Model:
    def __init__(self):
        self.session = Session()
        self.connection = engine.connect()

    def find_pk_order(self, key_value: int):
        return self.session.query(Order).filter_by(order_id=key_value).first()

    def find_fk_order(self, key_value: int, table_name: str):
        if table_name == "Customers":
            return self.session.query(Order).filter_by(customer_id=key_value).first()
        elif table_name == "Cars":
            return self.session.query(Order).filter_by(car_id=key_value).first()
        elif table_name == "Stuff":
            return self.session.query(Order).filter_by(stuff_id=key_value).first()
    
    def find_pk_customer(self, key_value: int):
        return self.session.query(Customer).filter_by(customer_id=key_value).first()

    def find_pk_car(self, key_value: int):
        return self.session.query(Car).filter_by(car_id=key_value).first()

    def find_pk_stuff(self, key_value: int):
        return self.session.query(Stuff).filter_by(stuff_id=key_value).first()

    def print_orders(self):
        return self.session.query(Order).order_by(Order.order_id.asc()).all()

    def print_customers(self):
        return self.session.query(Customer).order_by(Customer.customer_id.asc()).all()

    def print_cars(self):
        return self.session.query(Car).order_by(Car.car_id.asc()).all()

    def print_stuff(self):
        return self.session.query(Stuff).order_by(Stuff.stuff_id.asc()).all()

    def delete_data_order(self, order_id) -> None:
        self.session.query(Order).filter_by(order_id=order_id).delete()
        self.session.commit()

    def delete_data_customer(self, customer_id) -> None:
        self.session.query(Customer).filter_by(customer_id=customer_id).delete()
        self.session.commit()

    def delete_data_car(self, car_id) -> None:
        self.session.query(Car).filter_by(car_id=car_id).delete()
        self.session.commit()

    def delete_data_stuff(self, stuff_id) -> None:
        self.session.query(Stuff).filter_by(stuff_id=stuff_id).delete()
        self.session.commit()

    def update_data_order(self, order_id: int, customer_id: int, car_id: int, stuff_id: int,order_date: str) -> None:
        self.session.query(Order).filter_by(order_id=order_id) \
            .update({Order.customer_id: customer_id, Order.car_id: car_id,
                     Order.stuff_id: stuff_id,Order.order_date:order_date})
        self.session.commit()

    def update_data_customer(self, customer_id: int, customer_name: str, customer_surname: str, customer_telephone: str) -> None:
        self.session.query(Customer).filter_by(customer_id=customer_id) \
            .update({Customer.customer_name: customer_name, Customer.customer_surname: customer_surname, Customer.customer_telephone: customer_telephone})
        self.session.commit()

    def update_data_car(self, car_id: int, brand_name: str, model_name: str, year_of_manufacture: int) -> None:
        self.session.query(Car).filter_by(car_id=car_id) \
            .update({Car.brand_name: brand_name, Car.model_name: model_name, Car.year_of_manufacture: year_of_manufacture})
        self.session.commit()

    def update_data_stuff(self, stuff_id: int, stuff_surname: str, date_start_working: str ,stuff_telephone: str) -> None:
        self.session.query(Stuff).filter_by(stuff_id=stuff_id) \
            .update({Stuff.stuff_surname: stuff_surname, Stuff.date_start_working: date_start_working, Stuff.stuff_telephone: stuff_telephone})
        self.session.commit()

    def insert_data_order(self, order_id: int, customer_id: int, car_id: int, stuff_id: int, order_date: str) -> None:
        order = Order(order_id=order_id, customer_id=customer_id, car_id=car_id, stuff_id=stuff_id, order_date=order_date)
        self.session.add(order)
        self.session.commit()

    def insert_data_customer(self, customer_id: int, customer_name: str, customer_surname: str, customer_telephone: str) -> None:
        customer = Customer(customer_id=customer_id, customer_name=customer_name, customer_surname=customer_surname, customer_telephone=customer_telephone)
        self.session.add(customer)
        self.session.commit()

    def insert_data_car(self, car_id: int, brand_name: str, model_name: str, year_of_manufacture: str) -> None:
        car = Car(car_id=car_id, brand_name=brand_name, model_name=model_name, year_of_manufacture=year_of_manufacture)
        self.session.add(car)
        self.session.commit()

    def insert_data_stuff(self, stuff_id: int, stuff_surname: str, date_start_working: str, stuff_telephone: str) -> None:
        stuff = Stuff(stuff_id=stuff_id, stuff_surname=stuff_surname, date_start_working=date_start_working,stuff_telephone=stuff_telephone)
        self.session.add(stuff)
        self.session.commit()

    def car_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute("insert into public.\"Cars\""
                         "select (SELECT MAX(car_id)+1 FROM public.\"Cars\"), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) \
                         FROM generate_series(1, FLOOR(RANDOM()*(10-4)+4):: integer)), ''), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) \
                         FROM generate_series(1, FLOOR(RANDOM()*(10-4)+4):: integer)), ''), "
                         "FLOOR(RANDOM()*(100000-1)+1);")

    def customer_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute(
                "insert into public.\"Customers\" select (SELECT (MAX(customer_id)+1) FROM public.\"Customers\"), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''), "
                        
                         "(SELECT to_timestamp(1549634400+random()*70071999));")

    def order_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute(
                "insert into public.\"Orders\" select (SELECT MAX(order_id)+1 FROM public.\"Orders\"), "
                         "(SELECT customer_id FROM public.\"Customers\" LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(customer_id) FROM public.\"Customers\")-1)))), "
                         "(SELECT car_id FROM public.\"Cars\" LIMIT 1 OFFSET "
                         "(round(random() * ((SELECT COUNT(car_id) FROM public.\"Cars\")-1)))), "
                         "(SELECT stuff_id FROM public.\"Stuff\" LIMIT 1 OFFSET "
                         "(round(random() * ((SELECT COUNT(stuff_id) FROM public.\"Stuff\")-1)))), "
                         "(SELECT to_timestamp(1549634400+random()*70071999));")

    def stuff_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute("insert into public.\"Stuff\" select (SELECT MAX(stuff_id)+1 FROM public.\"Stuff\"), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(25-10)+10):: integer)), ''), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-4)+4):: integer)), ''), "
                         "(SELECT to_timestamp(1549634400+random()*70071999));")

    def search_data_two_tables(self):
        return self.session.query(Order) \
            .join(Stuff) \
            .filter(and_(
                Order.order_id.between(0, 10),
				Stuff.stuff_id.between(0, 2)
            )) \
            .all()

    def search_data_three_tables(self):
        return self.session.query(Order) \
            .join(Stuff).join(Car) \
            .filter(and_(
                Car.car_id.between(0, 5),
                Stuff.stuff_id.between(0, 2),
                Order.order_id.between(0, 10)
            )) \
            .all()

    def search_data_all_tables(self):
        return self.session.query(Order) \
            .join(Stuff).join(Customer).join(Car) \
            .filter(and_(
                Customer.customer_id.between(0, 4),
                Stuff.stuff_id.between(0, 2),
                Order.order_id.between(0, 10),
				Car.car_id.between(0, 5)
            )) \
            .all()

