import datetime
import psycopg2 as ps


class Model:
    def __init__(self):
        self.conn = None
        try:
            self.conn = ps.connect(
                database="car_showroom_nonrelative",
                user='postgres',
                password="qwerty",
                host='127.0.0.1',
                port="5432",
            )
        except(Exception, ps.DatabaseError) as error:
            print("[INFO] Error while working with Postgresql", error)

    def request(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return True
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def get(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return cursor.fetchall()
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def get_el(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return cursor.fetchone()
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def count(self, table_name: str):
        return self.get_el(f"select count(*) from public.\"{table_name}\"")

    def find(self, table_name: str, key_name: str, key_value: int):
        return self.get_el(f"select count(*) from public.\"{table_name}\" where {key_name}={key_value}")

    def max(self, table_name: str, key_name: str):
        return self.get_el(f"select max({key_name}) from public.\"{table_name}\"")

    def min(self, table_name: str, key_name: str):
        return self.get_el(f"select min({key_name}) from public.\"{table_name}\"")

    def print_cars(self) -> None:
        return self.get(f"SELECT * FROM public.\"Cars\"")

    def print_customers(self) -> None:
        return self.get(f"SELECT * FROM public.\"Customers\"")

    def print_orders(self) -> None:
        return self.get(f"SELECT * FROM public.\"Orders\"")

    def print_stuff(self) -> None:
        return self.get(f"SELECT * FROM public.\"Stuff\"")

    def delete_data(self, table_name: str, key_name: str, key_value) -> None:
        self.request(f"DELETE FROM public.\"{table_name}\" WHERE {key_name}={key_value};")

    def update_data_customers(self, key_value: int, customer_name: str, customer_surname: str, customer_telephone: str) -> None:
        self.request(f"UPDATE public.\"Customers\" SET customer_name=\'{customer_name}\', customer_surname =\'{customer_surname}\', customer_telephone=\'{customer_telephone }\', "
                     f"WHERE customer_id={customer_id};")

    def update_data_orders(self, key_value: int, customer_id: int, car_id: int, stuff_id: int, order_date: datetime.datetime) -> None:
        self.request(f"UPDATE public.\"Orders\" SET customer_id=\'{customer_id}\', car_id=\'{car_id}\', stuff_id=\'{stuff_id}\',"
                     f"order_date=\'{order_date}\' WHERE order_id={key_value};")

    def update_data_cars(self, key_value: int, brand_name: str, model_name: str, year_of_manufacture: int) -> None:
        self.request(f"UPDATE public.\"Cars\" SET brand_name=\'{brand_name}\', model_name=\'{model_name}\',"
                     f"year_of_manufacture=\'{year_of_manufacture}\' WHERE car_id={key_value};")

    def update_data_stuff(self, key_value: int, stuff_surname: str, date_start_working:datetime.datetime ,stuff_telephone:str) -> None:
        self.request(f"UPDATE public.\"Stuff\" SET stuff_surname=\'{stuff_surname}\', date_start_working=\'{date_start_working}\',"
                     f"stuff_telephone=\'{stuff_telephone}\' WHERE stuff_id={key_value};")

    def insert_data_cars(self, car_id: int, brand_name: str, model_name: str, year_of_manufacture: int) -> None:
        self.request(f"insert into public.\"Cars\" (car_id, brand_name , model_name , year_of_manufacture) "
                     f"VALUES ({car_id}, \'{brand_name}\', \'{model_name}\', \'{year_of_manufacture}\');")

    def insert_data_customers(self, customer_id: int, customer_name: str, customer_surname: str, customer_telephone: str) -> None:
        self.request(f"insert into public.\"Customers\" (customer_id, customer_name, customer_surname, customer_telephone) "
                     f"VALUES ({customer_id}, \'{customer_name}\', \'{customer_surname}\', \'{customer_telephone}\');")

    def insert_data_orders(self, order_id: int, customer_id: str, car_id: int, stuff_id: int,order_date:datetime.datetime) -> None:
        self.request(f"insert into public.\"Orders\" (order_id, customer_id, car_id, stuff_id,order_date) "
                     f"VALUES ({order_id}, \'{customer_id}\', \'{car_id}\', \'{stuff_id}\',\'{order_date}\');")

    def insert_data_stuff(self, stuff_id: int, stuff_surname: str, stuff_telephone: str,date_start_working:datetime.datetime) -> None:
        self.request(f"insert into public.\"Stuff\" (stuff_id, stuff_surname, stuff_telephone,date_start_working) "
                     f"VALUES ({stuff_id}, \'{stuff_surname}\', \'{stuff_telephone}\',\'{date_start_working}\');")

    def cars_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"Cars\""
                         "select (SELECT MAX(car_id)+1 FROM public.\"Cars\"), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) \
                         FROM generate_series(1, FLOOR(RANDOM()*(10-4)+4):: integer)), ''), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) \
                         FROM generate_series(1, FLOOR(RANDOM()*(10-5)+7):: integer)), ''), "
                         "FLOOR(RANDOM()*(100000-1)+1);")

    def customers_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"Customers\" select (SELECT (MAX(customer_id)+1) FROM public.\"Customers\"), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(11-2)+6):: integer)), ''), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(5-3)+1):: integer)), ''), "
                        
                         "(SELECT to_timestamp(1549634400+random()*70071999));")

    def orders_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"Orders\" select (SELECT MAX(order_id)+1 FROM public.\"Orders\"), "
                         "(SELECT customer_id FROM public.\"Customers\" LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(customer_id) FROM public.\"Customers\")-1)))), "
                         "(SELECT car_id FROM public.\"Cars\" LIMIT 1 OFFSET "
                         "(round(random() * ((SELECT COUNT(car_id) FROM public.\"Cars\")-1)))), "
                         "(SELECT stuff_id FROM public.\"Stuff\" LIMIT 1 OFFSET "
                         "(round(random() * ((SELECT COUNT(stuff_id) FROM public.\"Stuff\")-1)))), "
                         "(SELECT to_timestamp(1549634400+random()*70071999));")

    def stuff_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"Stuff\" select (SELECT MAX(stuff_id)+1 FROM public.\"Stuff\"), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(25-10)+2):: integer)), ''), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(7-4)+9):: integer)), ''), "
                         "(SELECT to_timestamp(1549634400+random()*70071999));")

    def search_data_two_tables(self, table1_name: str, table2_name: str, table1_key, table2_key,
                               search: str):
        return self.get(f"select * from public.\"{table1_name}\" as one inner join public.\"{table2_name}\" as two "
                        f"on one.\"{table1_key}\"=two.\"{table2_key}\" "
                        f"where {search}")

    def search_data_three_tables(self, table1_name: str, table2_name: str, table3_name: str,
                                 table1_key, table2_key, table3_key, table13_key,
                                 search: str):
        return self.get(f"select * from public.\"{table1_name}\" as one inner join public.\"{table2_name}\" as two "
                        f"on one.\"{table1_key}\"=two.\"{table2_key}\" inner join public.\"{table3_name}\" as three "
                        f"on three.\"{table3_key}\"=one.\"{table13_key}\""
                        f"where {search}")

    def search_data_all_tables(self, table1_name: str, table2_name: str, table3_name: str, table4_name: str,
                               table1_key, table2_key, table3_key, table13_key,
                               table4_key, table24_key,
                               search: str):
        return self.get(f"select * from public.\"{table1_name}\" as one inner join public.\"{table2_name}\" as two "
                        f"on one.\"{table1_key}\"=two.\"{table2_key}\" inner join public.\"{table3_name}\" as three "
                        f"on three.\"{table3_key}\"=one.\"{table13_key}\" inner join public.\"{table4_name}\" as four "
                        f"on four.\"{table4_key}\"=two.\"{table24_key}\""
                        f"where {search}")

