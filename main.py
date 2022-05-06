"""
SQL Database Practice

This simple database will store makes, models, years, license plates, states, and colors for cars.
"""

import sqlite3
from datetime import datetime, timedelta

def get_plate(cursor):
        cursor.execute("SELECT license_plate FROM cars")
        plates = []
        for record in cursor.fetchall():
            plate = record[0]
            plates.append(plate)
            print(f"{len(plates)}. {plate}")
        index = int(input("Select > "))
        assert index-1 >= 0
        return plates[index-1]

def get_update_info(cursor, plate):
    try:
        cursor.execute("SELECT * FROM cars WHERE license_plate = ?", (plate,))
        record = cursor.fetchall()
        retrieved_make = record[0][0]
        retrieved_model = record[0][1]
        retrieved_year = record[0][2]
        retrieved_state = record[0][3]
        retrieved_license_plate = record[0][4]
        retrieved_color = record[0][5]
        print(f"Current make is: {retrieved_make}. Type new value or press ENTER to keep current value.")
        make = input("Make: ")
        if make == "":
            make = retrieved_make
        
        print(f"Current model is: {retrieved_model}. Type new value or press ENTER to keep current value.")
        model = input("Model: ")
        if model == "":
            model = retrieved_model
        
        print(f"Current year is: {retrieved_year}. Type new value or press ENTER to keep current value.")
        year = input("Year: ")
        if year == "":
            year = retrieved_year
            print(f"year was not spcified, using old value: {retrieved_year}")
        year = int(year)
        print(f"saved year: {year}")

        print(f"Current state is: {retrieved_state}. Type new value or press ENTER to keep current value.")
        state = input("State: ")
        if state == "":
            state = retrieved_state
        
        print(f"Current license plate is: {retrieved_license_plate}. Type new value or press ENTER to keep current value.")
        license_plate = input("License plate: ")
        if license_plate == "":
            license_plate = retrieved_license_plate
        
        print(f"Current color is: {retrieved_color}. Type new value or press ENTER to keep current value.")
        color = input("Color: ")
        if color == "":
            color = retrieved_color

        time = cursor.execute("SELECT DATETIME()").fetchall()[0][0]

        different = make != retrieved_make or model != retrieved_model or year != retrieved_year or state != retrieved_state or\
        license_plate != retrieved_license_plate or color != retrieved_color

        return different, make, model, year, state, license_plate, color, time
    except:
        print("ERROR! Bad pay input")

# Connect to the database
with sqlite3.connect('records.db') as connection:
    cursor = connection.cursor()

    # Create table (if it does not already exist)
    cursor.execute("CREATE TABLE IF NOT EXISTS cars (make TEXT, model TEXT, year REAL, state TEXT, license_plate TEXT, color TEXT, time DATETIME)")
        

    choice = None
    while choice != "6":
        print()
        print("1) Display Cars")
        print("2) Add Car")
        print("3) Update Car Info")
        print("4) Delete Car")
        print("5) Get Car By Updated Time")
        print("6) Quit")
        choice = input("> ")
        print()
        if choice == "1":
            # Display Cars
            cursor.execute("SELECT * FROM cars ORDER BY year")
            print("{:>15}  {:>15}  {:>15} {:>15}  {:>15}  {:>15} {:>15}".format("Make", "Model", "Year", "State", "License plate", "Color", "Last updated"))
            for record in cursor.fetchall():
                print("{:>15}  {:>15}  {:>15} {:>15}  {:>15}  {:>15} {:>15}".format(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
        elif choice == "2":
            # Add New Car
            make = input("Make: ")
            model = input("Title: ")
            try:
                year = int(input("Year: "))
            except:
                print("ERROR! Bad year input")
            state = input("State: ")
            license_plate = input("License Plate: ")
            color = input("Color: ")
            time = datetime.now()
            cursor.execute("INSERT INTO cars VALUES (?, ?, ?, ?, ?, ?, ?)", (make, model, year, state, license_plate, color, time))
            connection.commit()
        elif choice == "3":
            # Update Cars
            try:
                plate = get_plate(cursor)
            except:
                print("ERROR! No Plate at provided index")
                continue
            try:
                update_info = get_update_info(cursor, plate)
                if update_info[0]:
                    cursor.execute("UPDATE cars SET make = ?, model = ?, year = ?, state = ?, license_plate = ?, color = ?, time = ? WHERE license_plate = ?", (
                        update_info[1], update_info[2], update_info[3], update_info[4], update_info[5], update_info[6], update_info[7], plate))
                    if cursor.rowcount == 0:
                        print("ERROR! Employee does not exist yet")
                    connection.commit()
                else:
                    print("No changes detected, not applying.")
            except:
                print("ERROR! Bad year input")

        elif choice == "4":
            # Delete Car
            try:
                license_plate = get_plate(cursor)
                cursor.execute("DELETE FROM cars WHERE license_plate = ?", (license_plate,))
                connection.commit()
            except:
                print("ERROR! No car at provided index")
        elif choice == "5":
            # Get car by update time
            try:
                days = int(input("How many days back: "))
                hours = int(input("How many hours back: "))
                minutes = int(input("How many minutes back: "))
                seconds = int(input("How many seconds back: "))
                time_cutoff = datetime.now() - timedelta(days=days,hours=hours,minutes=minutes,seconds=seconds)
                cursor.execute("SELECT * FROM cars WHERE time >= ?", (time_cutoff,))
                print("{:>15}  {:>15}  {:>15} {:>15}  {:>15}  {:>15} {:>15}".format("Make", "Model", "Year", "State", "License plate", "Color", "Last updated"))
                for record in cursor.fetchall():
                    print("{:>15}  {:>15}  {:>15} {:>15}  {:>15}  {:>15} {:>15}".format(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
            except:
                print("ERROR! Bad time input")
                continue
