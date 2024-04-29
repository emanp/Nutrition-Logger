#Author: Emanuelle Pelayo
#Date: April 7th, 2024
#CS457 HW #6
#Food Logger

import datetime
import psycopg

       

def logData(userFoodName, userDate, nutrientInfoList): 
    with psycopg.connect("dbname=postgres user=postgres password=AClife980 host=localhost port=5432") as connection:
        
        # Open a cursor to perform database operations
        with connection.cursor() as curs:
            
            for record in nutrientInfoList:
                nutrientNumber = record[1]
                nutrientName = record[0]
                amountOfNutrient = record[2]
                scaleOfAmount = record[3]
                
                query = ("""INSERT INTO userLog (foodname, nutrient_num, nutrient_name, date, "amountOfNutrient","scaleOfAmount") VALUES (%s, %s, %s, %s, %s, %s);""")
                
                curs.execute(query, (userFoodName, nutrientNumber, nutrientName, userDate, amountOfNutrient, scaleOfAmount))
        
            
        # Make the changes to the database persistent
        connection.commit()

        
def getNutrientIdAndFoodDescription(userFoodName): #food description = food name
    with psycopg.connect("dbname=postgres user=postgres password=AClife980 host=localhost port=5432") as connection:
    
        with connection.cursor() as curs:
            
            curs.execute("""SELECT nutrient.name, nutrient_id, amount, unit_name 
                FROM nutrient 
                JOIN (
                    SELECT description, nutrient_id, amount
                    FROM food 
                    JOIN food_nutrient ON food.fdc_id = food_nutrient.fdc_id 
                    WHERE description = %s
                ) AS subquery ON nutrient.id = subquery.nutrient_id;""", (userFoodName,))
                    
            nutrientInfoList = curs.fetchall()
                     
        return nutrientInfoList

            
def printUserLog():
    foodsEaten = []
    
    print ("--ENTER DATE YOU WANT NUTRITION VALUES FOR--")
    year = int(input("Enter a year: "))
    month = int(input("Enter a month: "))
    day = int(input("Enter a day: "))
    dateDesired = datetime.date(year, month, day)
    dateDesiredString = str(dateDesired)
    
    with psycopg.connect("dbname=postgres user=postgres password=AClife980 host=localhost port=5432") as connection:
        
        with connection.cursor() as curs:
            curs.execute ("""SELECT * FROM userLog where date = %s""", (dateDesiredString,))
            
            print ("\n--Nutrient values for " + dateDesiredString + "--")
            
            allRows = curs.fetchall()
            for record in allRows: 
                foodsEaten.append(record[1])    
            foodsEaten = list(set(foodsEaten)) #remove duplicate foods for that date
            
            for record in allRows: 
                food = record[1]
                
                #print the food name once, along with its nutrient values
                if food in foodsEaten:
                    print ("         YOU ATE: "+ food)
                    print ("----------"+"----------"+"----------"+"----------")
                    print ("         NUTRIENTS")
                    print ("----------"+"----------"+"----------"+"----------")
                    print (record[3]+ ": " +record[5]+" " + record[6])
                    foodsEaten.remove(food)
     
                else:
                    food = " "
                    print ("----------"+"----------"+"----------"+"----------")
                    print (record[3]+ ": " +record[5]+" " + record[6])
        
            print ("----------"+"----------"+"----------"+"----------")

                 
def main():
    
    while True:
        userOption = int(input("\nPress 1 to log Food \nPress 2 to print nutrient values\nPress 0 to EXIT \n"))
        
        
        match userOption:
            case 1:
                
                #get info from user
                food = str(input("Enter Food: "))
                year = int(input("Enter a year: "))
                month = int(input("Enter a month: "))
                day = int(input("Enter a day: "))
                dateEaten = datetime.date(year, month, day)
                dateEatenString = str(dateEaten)
                
                foodNutrientData = getNutrientIdAndFoodDescription(food)
                logData(food, dateEatenString, foodNutrientData)
                
                #Once added, let the user know
                print ("-----Logged!-----")
            
            case 2: #print log for a specific date
                printUserLog()
                
            case 0: 
                break
    
            case _: #user gives undesired input -.-
                print ("\n--Enter a valid option...--")
                continue


if __name__ == "__main__":
    main()








