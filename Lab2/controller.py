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

    def delete(self, table_name, key_name, value):
        t_name = self.v.valid.check_table_name(table_name)
        k_name = self.v.valid.check_pk_name(table_name, key_name)
        if t_name and k_name:
            count = self.m.find(t_name, k_name, value)
            k_val = self.v.valid.check_pk(value, count)
            if k_val:
                if t_name == 'Cars' or t_name == 'Customers' or t_name == 'Stuff':
                    count_p = self.m.find('Orders', k_name, value)[0]
                    if count_p:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data(table_name, key_name, k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
#                elif t_name == 'Shop':
#                    count_c = self.m.find('Catalog', k_name, value)[0]
#                    count_o = self.m.find('Order', k_name, value)[0]
#                    if count_c or count_o:
#                        self.v.cannot_delete()
#                    else:
#                        try:
#                            self.m.delete_data(table_name, key_name, k_val)
#                        except (Exception, Error) as _ex:
#                            self.v.sql_error(_ex)
                else:
                    try:
                        self.m.delete_data(table_name, key_name, k_val)
                    except (Exception, Error) as _ex:
                        self.v.sql_error(_ex)
            else:
                self.v.deletion_error()

    def update_customer(self, key: str, customer_name: str, customer_surname: str, customer_telephone: str):
        if self.v.valid.check_possible_keys('Customers', 'customer_id', key):
            count_p = self.m.find('Customers', 'customer_id', int(key))
#            p_val = self.v.valid.check_pk(key, count_p)
            try:
                self.m.update_data_product(p_val, customer_surname, customer_name,
                                           customer_telephone)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_cars(self, key: str, brand_name: str, model_name: str, year_of_manufacture: int):
        if self.v.valid.check_possible_keys('Cars', 'car_id', key):
            count_p = self.m.find('Cars', 'car_id', int(key))
#            p_val = self.v.valid.check_pk(key, count_p)       
            try:
#                arr = [int(x) for x in date.split(sep='.')]
                self.m.update_data_order(brand_name,model_name, year_of_manufacture)
 #                                        datetime.datetime(arr[0], arr[1], arr[2],
 #                                                          arr[3], arr[4], arr[5]))
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_orders(self, key: str, customer_id: int, car_id: int, stuff_id: int, order_date: str):
        if self.v.valid.check_possible_keys('Orders', 'order_id', key):
            count_s = self.m.find('Orders', 'order_id', int(key))
#            s_val = self.v.valid.check_pk(key, count_s)
        if self.v.valid.check_possible_keys('Customers', 'customer_id', customer_id):
            count_c = self.m.find('Customers', 'customer_id', int(customer_id))
            c_val = self.v.valid.check_pk(customer_id, count_c)
        if self.v.valid.check_possible_keys('Cars', 'car_id', car_id):
            count_pc = self.m.find('Cars', 'car_id', int(car_id))
            pc_val = self.v.valid.check_pk(car_id, count_pc)
        if self.v.valid.check_possible_keys('Stuff', 'stuff_id', stuff_id):
            count_p = self.m.find('Stuff', 'stuff_id', int(stuff_id))
            p_val = self.v.valid.check_pk(stuff_id, count_p)

        if s_val and c_val and pc_val and p_val:
            try:
                self.m.update_data_catalog(s_val,c_val, pc_val, p_val, order_date)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_stuff(self, key: str, stuff_surname: str, date_start_working:str ,stuff_telephone:str):
        if self.v.valid.check_possible_keys('Stuff', 'stuff_id', key):
            count_s = self.m.find('Stuff', 'stuff_id', int(key))
#            s_val = self.v.valid.check_pk(key, count_s)

        if s_val:
            try:
                self.m.update_data_shop(s_val, stuff_surname , stuff_telephone, date_start_working)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def insert_customer(self, key: str, customer_name: str, customer_surname: str, customer_telephone: str):
        if self.v.valid.check_possible_keys('Customers', 'customer_id', key):
            count_p = self.m.find('Customers', 'customer_id', int(key))[0]

        if (not count_p or count_p == (0,)) \
                and self.v.valid.check_possible_keys('Customers', 'customer_id', key):
            try:
                self.m.insert_data_product(int(key), customer_name , customer_surname ,
                                           customer_telephone)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_cars(self, key: str, brand_name: str, model_name: str, year_of_manufacture: int):
        if self.v.valid.check_possible_keys('Cars ', 'car_id', key):
            count_s = self.m.find('Cars', 'car_id', int(key))
#            s_val = self.v.valid.check_pk(key, count_s)

#        if s_val and self.v.valid.check_possible_keys('Cars', 'car_id', key) \
#                and self.v.valid.check_possible_keys('Cars', 'date', date):
            try:
#                arr = [int(x) for x in date.split(sep='.')]
                self.m.insert_data_order(int(key),brand_name ,model_name, year_of_manufacture)
#                                         datetime.datetime(arr[0], arr[1], arr[2],
#                                                           arr[3], arr[4], arr[5]))
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_orders(self, key: str, customer_id: int, car_id: int, stuff_id: int, order_date: str):
        if self.v.valid.check_possible_keys('Orders', 'order_id', key):
            count_s = self.m.find('Orders', 'order_id', int(key))
            s_val = self.v.valid.check_pk(key, count_s)
        if self.v.valid.check_possible_keys('Customers', 'customer_id', customer_id):
            count_c = self.m.find('Customers', 'customer_id', int(customer_id))[0]
            c_val = self.v.valid.check_pk(customer_id, count_c)
        if self.v.valid.check_possible_keys('Cars', 'car_id', car_id):
            count_pc = self.m.find('Cars', 'car_id', int(car_id))
            pc_val = self.v.valid.check_pk(car_id, count_pc)
        if self.v.valid.check_possible_keys('Stuff', 'stuff_id', stuff_id):
            count_p = self.m.find('Stuff', 'stuff_id', int(stuff_id))
            p_val = self.v.valid.check_pk(stuff_id, count_p)

        if (not count_c or count_c == (0,)) and s_val and c_val and pc_val and p_val \
                and self.v.valid.check_possible_keys('Orders', 'order_id', key):
#            try:
               # self.m.insert_data_catalog(int(key) , s_val, pc_val,p_val,order_date)
#            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_shop(self, key: str, stuff_surname: str, date_start_working:str ,stuff_telephone:str):
        if self.v.valid.check_possible_keys('Stuff', 'stuff_id', key):
            count_s = self.m.find('Stuff', 'stuff_id', int(key))[0]

        if (not count_s or count_s == (0,)) and self.v.valid.check_possible_keys('Stuff', 'stuff_id', key):
            try:
                self.m.insert_data_shop(int(key), stuff_surname,date_start_working, stuff_telephone  )
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def generate(self, table_name: str, n: int):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            if t_name == 'Cars':
                self.m.cars_data_generator(n)
            elif t_name == 'Customers':
                self.m.customers_data_generator(n)
            elif t_name == 'Orders':
                self.m.orders_data_generator(n)
            elif t_name == 'Stuff':
                self.m.stuff_data_generator(n)

    def search_two(self, table1_name: str, table2_name: str, table1_key: str, table2_key: str, search: str):
        t1_n = self.v.valid.check_table_name(table1_name)
        t2_n = self.v.valid.check_table_name(table2_name)
        if t1_n and self.v.valid.check_key_names(t1_n, table1_key) and t2_n \
                and self.v.valid.check_key_names(t2_n, table2_key):
            start_time = time.time()
            result = self.m.search_data_two_tables(table1_name, table2_name, table1_key, table2_key,
                                                   search)
            self.v.print_time(start_time)

            self.v.print_search(result)

    def search_three(self, table1_name: str, table2_name: str, table3_name: str,
                     table1_key: str, table2_key: str, table3_key: str, table13_key: str,
                     search: str):
        t1_n = self.v.valid.check_table_name(table1_name)
        t2_n = self.v.valid.check_table_name(table2_name)
        t3_n = self.v.valid.check_table_name(table3_name)
        if t1_n and self.v.valid.check_key_names(t1_n, table1_key) and self.v.valid.check_key_names(t1_n, table13_key) \
                and t2_n and self.v.valid.check_key_names(t2_n, table2_key) \
                and t3_n and self.v.valid.check_key_names(t3_n, table3_key) \
                and self.v.valid.check_key_names(t3_n, table13_key):
            start_time = time.time()
            result = self.m.search_data_three_tables(table1_name, table2_name, table3_name,
                                                     table1_key, table2_key, table3_key, table13_key,
                                                     search)
            self.v.print_time(start_time)
            self.v.print_search(result)

    def search_four(self, table1_name: str, table2_name: str, table3_name: str, table4_name: str,
                    table1_key: str, table2_key: str, table3_key: str, table13_key: str,
                    table4_key: str, table24_key: str,
                    search: str):
        t1_n = self.v.valid.check_table_name(table1_name)
        t2_n = self.v.valid.check_table_name(table2_name)
        t3_n = self.v.valid.check_table_name(table3_name)
        t4_n = self.v.valid.check_table_name(table2_name)
        if t1_n and self.v.valid.check_key_names(t1_n, table1_key) and self.v.valid.check_key_names(t1_n, table13_key) \
                and t2_n and self.v.valid.check_key_names(t2_n, table2_key) \
                and self.v.valid.check_key_names(t2_n, table24_key) \
                and t3_n and self.v.valid.check_key_names(t3_n, table3_key) \
                and self.v.valid.check_key_names(t3_n, table13_key) \
                and t4_n and self.v.valid.check_key_names(t4_n, table4_key) \
                and self.v.valid.check_key_names(t4_n, table24_key):

            start_time = time.time()
            result = self.m.search_data_all_tables(table1_name, table2_name, table3_name, table4_name,
                                                   table1_key, table2_key, table3_key, table13_key,
                                                   table4_key, table24_key,
                                                   search)
            self.v.print_time(start_time)
            self.v.print_search(result)
