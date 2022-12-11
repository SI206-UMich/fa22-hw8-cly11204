#Name: Caitlin Yeung 
#SI 206 

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
import numpy as np

def get_restaurant_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. The key:value pairs should be the name, category, building, and rating
    of each restaurant in the database.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    
    #cur.execute('SELECT restaurants.name, categories.category FROM restaurants JOIN categories ON restaurants.category_id = categories.id')
    data = cur.execute ('SELECT restaurants.name, categories.category, buildings.building, restaurants.rating FROM restaurants JOIN categories ON restaurants.category_id = categories.id JOIN buildings ON restaurants.building_id = buildings.id')    

    #cur.execute ('SELECT restaurants.name, restaurants.category_id, restaurants.building_id, restaurants.rating, categories.category, buildings.building FROM restaurants  JOIN categories ON restaurants.category_id = categories.category  JOIN buildings ON restaurants.building_id = buildings.building')    
    result=cur.fetchall()
    
    header_list = []
    restaurant_list = []

    for column in data.description:
        header_list.append(column[0])

    for restaurant in result:
        for index, item in enumerate(restaurant):
            dict_of_restaurant = {}

            dict_of_restaurant[header_list[index]] = restaurant[index]
            restaurant_list.append(dict_of_restaurant)
    print (restaurant_list)
    return restaurant_list

def barchart_restaurant_categories(db_filename):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the counts of each category.
    """

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS CopyRestaurants')
    cur.execute('CREATE TABLE CopyRestaurants AS SELECT restaurants.name, categories.category, buildings.building, restaurants.rating FROM restaurants, categories, buildings WHERE restaurants.category_id = categories.id AND restaurants.building_id = buildings.id')

    #for dictionary --> category_list
    dict_of_cuisines = {}
    cur.execute('SELECT category, COUNT(*) AS cuisines FROM CopyRestaurants GROUP BY category')
    data = cur.fetchall()

    for item in data:
        dict_of_cuisines[item[0]] = item[1]

    N = len(dict_of_cuisines)
    ind = np.arange(N)

    cuisines = list(dict_of_cuisines.keys())
    amount_of_restaurants = list(dict_of_cuisines.values())

    fig = plt.figure()

    
    plt.barh(cuisines, sorted(amount_of_restaurants))

    plt.xlabel("Number of Restaurants")
    plt.ylabel("Restaurant Categories")
    plt.title("Type of Restaurant on South University Ave")
    plt.show()

    return dict_of_cuisines

#EXTRA CREDIT
def highest_rated_category(db_filename):#Do this through DB as well
    """
    This function finds the average restaurant rating for each category and returns a tuple containing the
    category name of the highest rated restaurants and the average rating of the restaurants
    in that category. This function should also create a bar chart that displays the categories along the y-axis
    and their ratings along the x-axis in descending order (by rating).
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    cur.execute('SELECT category, AVG(rating) FROM CopyRestaurants GROUP BY category')
    avg = cur.fetchall()
    print(avg)
    
    max = 0
    max_name = ""
    for avg_per_cuisine in avg: 
        if avg_per_cuisine[1] > max: 
            max_name = avg_per_cuisine[0]
            max = avg_per_cuisine[1]

    tup_of_highest_rating = (max_name,max)

    N = len(avg)
    ind = np.arange(N)

    cuisines = []
    avg_amount_cuisines = []

    for cuisine in sorted(avg,key = lambda x:x[1]): 
        cuisines.append(cuisine[0])
        avg_amount_cuisines.append(cuisine[1])

    fig = plt.figure(figsize=(12,6))
    
    plt.barh(cuisines, sorted(avg_amount_cuisines))

    plt.xlabel("Ratings")
    plt.ylabel("Categories")
    plt.title("Average Restaurant Ratings by Category")
    plt.show()
    print(tup_of_highest_rating)
    return tup_of_highest_rating
    

#Try calling your functions here
def main():
    get_restaurant_data("South_U_Restaurants.db")
    #print(barchart_restaurant_categories("South_U_Restaurants.db"))
    highest_rated_category("South_U_Restaurants.db")

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'name': 'M-36 Coffee Roasters Cafe',
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.best_category = ('Deli', 4.6)

    def test_get_restaurant_data(self):
        rest_data = get_restaurant_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, list)
        self.assertEqual(rest_data[0], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_barchart_restaurant_categories(self):
        cat_data = barchart_restaurant_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_highest_rated_category(self):
        best_category = highest_rated_category('South_U_Restaurants.db')
        self.assertIsInstance(best_category, tuple)
        self.assertEqual(best_category, self.best_category)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
