import psycopg2
from psycopg2 import Error
import model
import view
import datetime
import time


class Controller:
    def __init__(self):
        self.v = view.View()
        self.m = model.Model()

    def printf(self, table_name):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            if t_name == 'Cars':
                self.v.print_cars(self.m.print_cars())
            elif t_name == 'Customers':
                self.v.print_customers(self.m.print_customers())
            elif t_name == 'Orders':
                self.v.print_orders(self.m.print_orders())
            elif t_name == 'Stuff':
                self.v.print_stuff(self.m.print_stuff())

    def delete(self, table_name, value):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            k_val = self.v.valid.check_pk(value)
            count = 0
            if t_name == 'Orders' and k_val:
                count = self.m.find_pk_order(k_val)
            elif t_name == 'Customers' and k_val:
                count = self.m.find_pk_customer(k_val)
            elif t_name == 'Cars' and k_val:
                count = self.m.find_pk_car(k_val)
            elif t_name == 'Stuff' and k_val:
                count = self.m.find_pk_stuff(k_val)

            if count:
                if t_name == 'Customers' or t_name == 'Cars' or t_name == 'Stuff':
                    count_p = self.m.find_fk_order(k_val, t_name)
                    if count_p:
                        self.v.cannot_delete()
                    else:
                        try:
                            if t_name == 'Customers':
                                self.m.delete_data_customer(k_val)
                            elif t_name == 'Cars':
                                self.m.delete_data_car(k_val)
                            elif t_name == 'Stuff':
                                self.m.delete_data_stuff(k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
#"""                elif t_name == 'Shop':
#                    count_c = self.m.find_fk_catalog(k_val)
#                    count_o = self.m.find_fk_order(k_val)
#                    if count_c or count_o:
#                        self.v.cannot_delete()
#                    else:
#                        try:
#                            self.m.delete_data_shop(k_val)
#                        except (Exception, Error) as _ex:
#                            self.v.sql_error(_ex)
#"""							
            else:
                    try:
                        self.m.delete_data_order(k_val)
                    except (Exception, Error) as _ex:
                        self.v.sql_error(_ex)
        else:
                self.v.deletion_error()

    def update_customer(self, key: str, customer_name: str, customer_surname: str, customer_telephone: str):
        if self.v.valid.check_possible_keys('Customers', 'customer_id', key):
            count_p = self.m.find_pk_customer(int(key))
            p_val = self.v.valid.check_pk(key)
#			p_val=1
        if count_p and p_val:
            try:
                self.m.update_data_customer(p_val, customer_name, customer_surname,
                                           customer_telephone)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_cars(self, key: str, brand_name: str, model_name: str, year_of_manufacture: int):
        if self.v.valid.check_possible_keys('Cars', 'car_id', key):
            count_s = self.m.find_pk_car(int(key))
            s_val = self.v.valid.check_pk(key)
#			s_val = 1
        if count_s and \
                s_val and \
                self.v.valid.check_possible_keys('Cars', 'car_id', key):
            try:
                self.m.update_data_car(s_val, brand_name, model_name, year_of_manufacture)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_orders(self, key: str, customer_id: int, car_id: int, stuff_id: int, order_date: str):
        if self.v.valid.check_possible_keys('Orders', 'order_id', key):
            count_s = self.m.find_pk_order(int(key))
            s_val = self.v.valid.check_pk(key)
        if self.v.valid.check_possible_keys('Customers', 'customer_id', customer_id):
            count_c = self.m.find_pk_customer(int(customer_id))
            c_val = self.v.valid.check_pk(key)
        if self.v.valid.check_possible_keys('Cars', 'car_id', car_id):
            count_pc = self.m.find_pk_car(int(car_id))
            pc_val = self.v.valid.check_pk(car_id)
        if self.v.valid.check_possible_keys('Stuff', 'stuff_id', stuff_id):
            count_p = self.m.find_pk_stuff(int(stuff_id))
            p_val = self.v.valid.check_pk(stuff_id)

        if count_s and count_c and count_pc and count_p and \
                s_val and c_val and pc_val and p_val:
            try:
                self.m.update_data_order(s_val, c_val, pc_val, p_val, order_date)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_stuff(self, key: str, stuff_surname: str, date_start_working:str ,stuff_telephone:str):
        if self.v.valid.check_possible_keys('Stuff', 'stuff_id', key):
            count_s = self.m.find_pk_stuff(int(key))
            s_val = self.v.valid.check_pk(key)

        if count_s and s_val:
            try:
                self.m.update_data_stuff(s_val, stuff_surname, date_start_working,stuff_telephone)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def insert_customer(self, key: str, customer_name: str, customer_surname: str, customer_telephone: str):
        if self.v.valid.check_possible_keys('Customers', 'customer_id', key):
            count_p = self.m.find_pk_customer(int(key))

        if (not count_p) \
                and self.v.valid.check_possible_keys('Customers', 'customer_id', key):
            try:
                self.m.insert_data_customer(int(key), title, float(price),
                                           category, c_val, o_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_cars(self, key: str, brand_name: str, model_name: str, year_of_manufacture: int):
#        if self.v.valid.check_possible_keys('Cars ', 'car_id', key):
            count_o = self.m.find_pk_car(int(key))

            if (not count_o):
                try:
                    self.m.insert_data_car(int(key), brand_name, model_name,year_of_manufacture)
                except (Exception, Error) as _ex:
                    self.v.sql_error(_ex)
#        else:
#            self.v.insertion_error()

    def insert_orders(self, key: str, customer_id: int, car_id: int, stuff_id: int, order_date: str):
        if self.v.valid.check_possible_keys('Orders', 'order_id', key):
            count_c = self.m.find_pk_order(int(key))
        if self.v.valid.check_possible_keys('Customers', 'customer_id', customer_id):
            count_s = self.m.find_pk_order(int(key))
            s_val = self.v.valid.check_pk(key)
        if self.v.valid.check_possible_keys('Cars', 'car_id', car_id):
            count_pc = self.m.find_pk_car(int(car_id))
            pc_val = self.v.valid.check_pk(car_id)
        if self.v.valid.check_possible_keys('Stuff', 'stuff_id', stuff_id):
            count_p = self.m.find_pk_stuff(int(stuff_id))
            p_val = self.v.valid.check_pk(stuff_id)

        if (not count_c) and count_s and count_pc and s_val and pc_val \
                and count_p and p_val:
            try:
                self.m.insert_data_order(int(key), s_val, pc_val, p_val,order_date)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_stuff(self, key: str, stuff_surname: str, date_start_working:str ,stuff_telephone:str):
        if self.v.valid.check_possible_keys('Stuff', 'stuff_id', key):
            count_s = self.m.find_pk_stuff(int(key))

        if (not count_s):
            try:
                self.m.insert_data_stuff(int(key), stuff_surname, date_start_working, stuff_telephone)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def generate(self, table_name: str, n: int):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            if t_name == 'Cars':
                self.m.car_data_generator(n)
            elif t_name == 'Customers':
                self.m.customer_data_generator(n)
            elif t_name == 'Orders':
                self.m.order_data_generator(n)
            elif t_name == 'Stuff':
                self.m.stuff_data_generator(n)

    def search_two(self):
        result = self.m.search_data_two_tables()
        self.v.print_search(result)

    def search_three(self):
        result = self.m.search_data_three_tables()
        self.v.print_search(result)

    def search_all(self):
        result = self.m.search_data_all_tables()
        self.v.print_search(result)
