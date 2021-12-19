import controller as con
from psycopg2 import Error
import sys

c = con.Controller()

try:
    command = sys.argv[1]
except IndexError:
    c.v.no_command()
else:
    if command == 'print_table':
        try:
            name = sys.argv[2]
        except IndexError:
            c.v.argument_error()
        else:
            c.printf(name)

    elif command == 'delete_record':
        try:
            args = {"name": sys.argv[2], "val": sys.argv[3]}
        except IndexError:
            c.v.argument_error()
        else:
            c.delete(args["name"], args["val"])

    elif command == 'update_record':
        try:
            args = {"name": sys.argv[2], "key": sys.argv[3]}
            if args["name"] == 'Cars':
                args["brand_name"], args["model_name"], args["year_of_manufacture"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            elif args["name"] == 'Customers':
                args["customer_name"], args["customer_surname"], args["customer_telephone"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            elif args["name"] == 'Orders':
                args["customer_id"], args["car_id"], args["stuff_id"], args["order_date"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]
            elif args["name"] == 'Stuff':
                args["stuff_surname"], args["stuff_telephone"], args["date_start_working"]= \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            else:
                c.v.wrong_table()
        except IndexError:
            c.v.argument_error()
        else:
            if args["name"] == 'Cars':
                c.update_cars(args["key"], args["brand_name"], args["model_name"],
                                 args["year_of_manufacture"])
            elif args["name"] == 'Customers':
                c.update_customers(args["key"], args["customer_name"], args["customer_surname"], args["customer_telephone"])
            elif args["name"] == 'Orders':
                c.update_orders(args["key"], args["customer_id"], args["car_id"],args["stuff_id"], args["order_date"])
            elif args["name"] == 'Stuff':
                c.update_stuff(args["key"], args["stuff_surname"], args["stuff_telephone"], args["date_start_working"])

    elif command == 'insert_record':
        try:
            args = {"name": sys.argv[2], "key": sys.argv[3]}
            if args["name"] == 'Cars':
                args["brand_name"], args["model_name"], args["year_of_manufacture"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            elif args["name"] == 'Customers':
                args["customer_name"], args["customer_surname"], args["customer_telephone"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            elif args["name"] == 'Orders':
                args["customer_id"], args["car_id"],args["stuff_id"], args["order_date"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]
            elif args["name"] == 'Stuff':
                args["stuff_surname"], args["stuff_telephone"], args["date_start_working"]  = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            else:
                c.v.wrong_table()
        except IndexError:
            c.v.argument_error()
        else:
            if args["name"] == 'Cars':
                c.insert_cars(args["key"], args["brand_name"], args["model_name"],
                                 args["year_of_manufacture"])
            elif args["name"] == 'Customers':
                c.insert_customer(args["key"], args["customer_name"], args["customer_surname"], args["customer_telephone"])
            elif args["name"] == 'Orders':
                c.insert_orders(args["key"], args["customer_id"], args["car_id"], args["stuff_id"], args["order_date"])
            elif args["name"] == 'Stuff':
                c.insert_stuff(args["key"], args["stuff_surname"], args["stuff_telephone"], args["date_start_working"])

    elif command == 'generate_randomly':
        try:
            args = {"name": sys.argv[2], "n": int(sys.argv[3])}
        except (IndexError, Exception):
            print(Exception, IndexError)
        else:
            c.generate(args["name"], args["n"])

    elif command == 'search_records':
        while True:
            search_num = c.v.get_search_num()
            try:
                search_num = int(search_num)
            except ValueError:
                c.v.invalid_search_num()
            else:
                if search_num in [2, 3, 4]:
                    break
                else:
                    c.v.invalid_search_num()
        if search_num == 2:
            c.search_two()
        elif search_num == 3:
            c.search_three()
        elif search_num == 4:
            c.search_all()

    elif command == 'help':
        c.v.print_help()
    else:
        c.v.wrong_command()
