import datetime


class Validator:
    def __init__(self):
        self.error = ''
        self.er_flag = False

    def check_table_name(self, arg: str):
        if arg in ['Cars', 'Customers', 'Orders', 'Stuff']:
            return arg
        else:
            self.er_flag = True
            self.error = f'table {arg} does not exist in the database'
            print(self.error)
            return False

    def check_pkey_value(self, arg: str, min_val: int, max_val: int):
        try:
            value = int(arg)
        except ValueError:
            self.er_flag = True
            self.error = f'{arg} is not correct primary key value'
            print(self.error)
            return 0
        else:
            if min_val <= value <= max_val:
                return value
            else:
                self.er_flag = True
                self.error = f'{arg} is not existing primary key value'
                print(self.error)
                return 0

    def check_pk_name(self, table_name: str, key_name: str):
        if table_name == 'Cars' and key_name == 'car_id' \
                or table_name == 'Customers' and key_name == 'customer_id' \
                or table_name == 'Orders' and key_name == 'order_id' \
                or table_name == 'Stuff' and key_name == 'stuff_id':
            return key_name
        else:
            self.er_flag = True
            self.error = f'key {key_name} is not a primary key of table {table_name}'
            print(self.error)
            return False

    def check_pk(self, val):
        try:
            value = int(val)
            return value
        except ValueError:
            self.er_flag = True
            self.error = f'{val} is not correct primary key value'
            print(self.error)
            return 0

    def check_key_names(self, table_name: str, key: str):
        if table_name == 'Cars' and key in ['car_id', 'brand_name', 'model_name', 'year_of_manufacture']:
            return True
        elif table_name == 'Customers' and key in ['customer_id', 'customer_name', 'customer_surname', 'customer_telephone']:
            return True
        elif table_name == 'Orders' and key in ['order_id', 'customer_id', 'car_id', 'stuff_id','order_date']:
            return True
        elif table_name == 'Stuff' and key in ['stuff_id', 'stuff_surname', 'stuff_telephone','date_start_working']:
            return True
        else:
            self.er_flag = True
            self.error = f'{key} is not correct name for {table_name} table'
            print(self.error)
            return False

    def check_possible_keys(self, table_name: str, key: str, val):
        if table_name == 'Cars':
            if key in ['car_id']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key in ['brand_name', 'model_name']:
                return True
            elif key == 'year_of_manufacture':
                try:
                    value = float(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct year_of_manufacture value'
                    print(self.error)
                    return False
                else:
                    return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for Cars table'
                print(self.error)
                return False
        elif table_name == 'Customers':
            if key in ['customer_id']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key in ['customer_name','customer_surname']:
                return True
            elif key in ['customer_telephone']:
                try:
                    arr = [int(x) for x in val.split(sep='.')]
                    datetime.datetime(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5])
                except TypeError:
                    self.er_flag = True
                    self.error = f'{val} is not correct customer_telephone value'
                    print(self.error)
                    return False
                else:
                    return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for Customers table'
                print(self.error)
                return False
        elif table_name == 'Orders':
            if key in ['order_id', 'customer_id', 'car_id']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key == 'order_date':
                return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for Orders table'
                print(self.error)
                return False
        elif table_name == 'Stuff':
            if key == 'stuff_id':
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key in ['stuff_surname', 'stuff_telephone','date_start_working']:
                return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for Stuff table'
                print(self.error)
                return False
