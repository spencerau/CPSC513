#import MySQL and Redis
import mysql.connector
import redis
from dotenv import load_dotenv
import os
from datetime import date


load_dotenv()

#Make MySQL Connection
conn = mysql.connector.connect(host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    auth_plugin='mysql_native_password',
    database = "MyCompany")

#create MySQL cursor object
cur_obj = conn.cursor()

#Make Redis Connection
rconn = redis.Redis(host='localhost', port=6379, decode_responses=True)


def all_employee_select_cache():
    #execute query and return result
    if (rconn.scard('set:all_employee_results') != 0):
        print("Using cache")
        results = rconn.smembers('set:all_employee_results')
        all_employee_results = [int(i) for i in results]
        print(f"CACHE: {all_employee_results}")

    else: # not in cache
        # get all employees from system
        all_employee_select = '''
        SELECT employee_id
        FROM Employee;
        '''
        print("Using MySQL Query")
        cur_obj.execute(all_employee_select)
        results = cur_obj.fetchall()
        #convert from 2D array to 1D array
        all_employee_results = [i[0] for i in results]
        print(f"MySQL: {all_employee_results}")
        for i in all_employee_results:
            rconn.sadd('set:all_employee_results', i)
    
    return all_employee_results


def single_employee_select_cache(ee_id):

    if (rconn.hexists(f'employee:{ee_id}', 'employee_id')):
        print(f"USING CACHE TO SEARCH FOR EMPLOYEE {ee_id}")
        result = rconn.hgetall(f'employee:{ee_id}')
        print (result)
    else: # need to execute MySQL query
        cur_obj.execute("SHOW COLUMNS FROM Employee;")
        columns = cur_obj.fetchall()

        columns = [i[0] for i in columns]

        print(f"USING MySQL TO SEARCH FOR EMPLOYEE {ee_id}")
        single_employee_select = '''
        SELECT *
        FROM Employee
        WHERE employee_id = %s;
        '''
        cur_obj.execute(single_employee_select, (ee_id,))
        result = cur_obj.fetchall()

        # hash maps are fucking stupid and this code is scuffed
        # store in redis
        for i in range(len(columns)):
            # check if its a date item aka either hire_date or term_date
            key = columns[i]
            value = result[0][i]
            # check if the value is NULL
            if value is None:
                value = 'None'
            # check if its hire_date or term_date as date objects seem to be fucky
            if key in ('hire_date', 'term_date'):
                # need to also check if its NULL for something like term_date etc
                if value is not None and isinstance(value, date):
                    value = value.strftime('%Y-%m-%d')
                else:
                    value = 'None'
            rconn.hset(f'employee:{ee_id}', key = key, value = value)
        
        print_results(result)

    return result


# function to look up an employee in the MyCompany Database
def employee_lookup():

    all_employee_results = all_employee_select_cache()

    # prompt user for value to search
    print("Enter an Employee ID to return their record: ")

    ee_id = get_choice(all_employee_results)

    result = single_employee_select_cache(ee_id)
    rconn.sadd("set:employees_searched", ee_id)

    return


def redis_lookup():
    print("Employees searched this session: ")
    print(rconn.smembers("set:employees_searched"))
    return


# function checks for user input given a list of choices
@staticmethod
def get_choice(lst):
    choice = input("Enter choice number: ")
    while choice.isdigit() == False:
        print("Incorrect option. Try again")
        choice = input("Enter choice number: ")

    while int(choice) not in lst:
        print("Incorrect option. Try again")
        choice = input("Enter choice number: ")
    return int(choice)


# function parses a string and converts to appropriate type
@staticmethod
def convert(value):
    types = [int,float,str] # order needs to be this way
    if value == '':
        return None
    for t in types:
        try:
            return t(value)
        except:
            pass


# function prints a list of strings nicely
@staticmethod
def print_results(lst):
    for i in lst:
        print(i)
    print("")


def clear_cache():
    print("Clearing cache")
    rconn.delete("set:employees_searched")
    rconn.delete("set:all_employee_results")
    #rconn.delete("employee:*")
    # USED CHATGPT for this to delete from HashMaps in Redis-Py
    # Fetch all keys that match the pattern
    keys = rconn.keys('employee:*')

    # Delete all matching keys
    if keys:
        rconn.delete(*keys)


def main():
    print('Welcome to the employee records system.')

    while True:
        print('''
        Which action would you like to take?
            1. Search for an employee record
            2. View all employees searched for this session
            3. Exit
        ''')
        user_choice = get_choice([1, 2, 3])
        if user_choice == 1:
            employee_lookup()
        if user_choice == 2:
            redis_lookup()
        if user_choice == 3:
            #TODO: Clear out the user session information in Redis here
            clear_cache()
            print("Goodbye!")
            break


if __name__ == '__main__':
    main()


#Print out connection to verify and close
cur_obj.close()
conn.close()