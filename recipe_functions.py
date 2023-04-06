import db_base as db


#-----------------------------------------------------------------------------------------------------------------------
class Recipe(db.DBbase):  #parent class
    def __init__(self):
        super().__init__("recipe_db.db")


    # this method adds a recipe's properties to the db and then invokes the add_ingredient method
    def add(self, name, preptime, cooktime, difficulty, instructions):
        try:
            category = input("Please select a category for your recipe: \n1. Appetizer\n2. Salad\n3. Entree\n4. Dessert\n5. Drink\n")
            super().connect()
            super().get_cursor.execute("""INSERT INTO Recipe(name, preptime, cooktime, difficulty, category_id,instructions) VALUES (?,?,?,?,?,?);""", (name, preptime, cooktime, difficulty, category, instructions))
            #r_id is the recipe_id that will get passed into the add_ingredients method
            r_id = super().get_cursor.execute("SELECT id FROM Recipe WHERE name = ?", (name,)).fetchone()
            super().get_connection.commit()
            super().close_db()
            print("Now lets add the recipe's ingredients.")
            #r_id is passed to link ingredients to recipe they belong to
            self.add_ingredient(r_id[0])

        except Exception as x:
            print("Uh oh! An error occurred:", x)


    #this method adds ingredients to the db and uses recipe_id to link them to their respective recipe
    def add_ingredient(self, recipe_id):
        try:
            super().connect()
            #This loop will repeat until the user has no more ingredients to add
            while True:
                ing = input("Please enter the name of the ingredient or type 'exit': ").lower()
                if ing.lower() == "exit":
                    super().close_db()
                    print("Ingredients added successfully\n")
                    break
                else:
                    measure = input("How much of that ingredient is needed? ").lower()
                    super().get_cursor.execute("""INSERT INTO Ingredient(name, measurement, recipe_id) VALUES (?,?,?);""", (ing, measure, recipe_id))
                    super().get_connection.commit()
        except Exception as x:
            print("Oopsie! An error occurred:", x)


    #this method updates the properties of a recipe
    def update(self, id, name, preptime, cooktime, difficulty, instructions):
        try:
            category = input("Please select a category for the recipe you are updating: \n1. Appetizer\n2. Salad\n3. Entree\n4. Dessert\n5. Drink\n")
            super().connect()
            super().get_cursor.execute("UPDATE Recipe SET name = ?, preptime = ?, cooktime = ?, difficulty = ?, category_id = ?, instructions = ? WHERE id = ?;", (name, preptime, cooktime, difficulty, category, instructions, id))
            super().get_connection.commit()
            super().close_db()
            print("Updated recipe properties successfully")
            #print the updated version of the recipe
            print(self.fetch(recipe_id=id))
        except Exception as x:
            print("Woopsie! An error has occurred:", x)

    #this method fetches single or multiple rows of data from the db depending on parameters provided
    def fetch(self, recipe_id=None):
        try:
            super().connect()
            if recipe_id is not None:  #if recipe_id provided, fetch that specific record
                return super().get_cursor.execute("SELECT * FROM Recipe WHERE id = ?;", (recipe_id,)).fetchone()
            else:  #if no recipe_id provided, fetch all recipes
                return super().get_cursor.execute("SELECT id, name, difficulty FROM Recipe;").fetchall()
        except Exception as x:
            print("Ah man... An error occurred:", x)
        finally:
            super().close_db()

    #this method fetches all ingredients linked to the specified recipe_id
    def fetch_ing(self, recipe_id):
        try:
            super().connect()
            return super().get_cursor.execute("SELECT name, measurement FROM Ingredient WHERE recipe_id = ?;", (recipe_id,)).fetchall()
        except Exception as x:
            print("Ah man... An error occurred:", x)
        finally:
            super().close_db()

    #this method deletes the recipe that has specified recipe_id, it then deletes linked ingredients as well
    def delete(self, recipe_id):
        try:
            super().connect()
            super().get_cursor.execute("DELETE FROM Recipe WHERE id = ?;", (recipe_id,))
            super().get_cursor.execute("DELETE FROM Ingredient WHERE recipe_id = ?;", (recipe_id,))
            super().get_connection.commit()
            super().close_db()
            print("The recipe and its ingredients was removed successfully")
        except Exception as x:
            print("Oh shoot... An error occurred:", x)

    #this method only deletes ingredients tied to a recipe, but leaves recipe intact
    def delete_ing(self, recipe_id):
        try:
            super().connect()
            super().get_cursor.execute("DELETE FROM Ingredient WHERE recipe_id = ?;", (recipe_id,))
            super().get_connection.commit()
            super().close_db()
        except Exception as x:
            print("Well butter my butt and call me a biscuit.  An error occurred: ", x)

    #this method fetches all ingredients that use the specified ingredient (i.e. recipes that use butter)
    def search_by_ingredient(self, ingredient):
        try:
            super().connect()
            return super().get_cursor.execute("SELECT Recipe.id, Recipe.name, Recipe.difficulty FROM Recipe JOIN Ingredient ON Recipe.id = Ingredient.recipe_id WHERE Ingredient.name = ?;", (ingredient,)).fetchall()
        except Exception as x:
            print("Well gosh... An error occurred:", x)
        finally: super().close_db()

    #this method fetches all ingredients that are under the specified category
    def search_by_category(self, category):
        try:
            super().connect()
            return super().get_cursor.execute("SELECT id, name, difficulty FROM Recipe WHERE category_id = ?;", (category,)).fetchall()
        except Exception as x:
            print("Gosh!!! An error occurred:", x)
        finally: super().close_db()

    #this method resets the recipe and ingredient tables if needed.
    #Category table remains intact because those values do not change.
    def reset_database(self):
        sql = """
            DROP TABLE IF EXISTS "Recipe";
            CREATE TABLE IF NOT EXISTS "Recipe" (
                "id"	INTEGER NOT NULL UNIQUE,
                "name"	TEXT NOT NULL UNIQUE,
                "preptime"	BLOB NOT NULL,
                "cooktime"	TEXT NOT NULL,
                "difficulty"	TEXT NOT NULL,
                "category_id"	INTEGER NOT NULL,
                "instructions"	BLOB NOT NULL,
                "cook_setting"	TEXT,
                "vent_type"	TEXT,
                "baking_dish"	TEXT,
                "high_alt_adj"	BLOB,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
            DROP TABLE IF EXISTS "Ingredient";
            CREATE TABLE IF NOT EXISTS "Ingredient" (
                "id"	INTEGER NOT NULL UNIQUE,
                "name"	TEXT NOT NULL,
                "measurement"	TEXT NOT NULL,
                "recipe_id"	INTEGER NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """
        super().execute_script(sql)


#-----------------------------------------------------------------------------------------------------------------------
#this is the childclass of parentclass Recipe.  It includes instapot cook settings and ventilation type
#instructions not needed by traditional recipes.
class Instapot(Recipe):
    def __init__(self):
        super().__init__()

    #this overwrites the add method in the parent class to include settings and vent_type variables
    def add(self, name, preptime, cooktime, difficulty, instructions, settings, vent_type):
        try:
            category = input("Please select a category for your Instapot recipe: \n1. Appetizer\n2. Salad\n3. Entree\n4. Dessert\n5. Drink\n")
            super().connect()
            super().get_cursor.execute("INSERT INTO Recipe(name, preptime, cooktime, difficulty, category_id,instructions, cook_setting, vent_type) VALUES (?,?,?,?,?,?,?,?);", (name, preptime, cooktime, difficulty, category, instructions, settings, vent_type))
            r_id = super().get_cursor.execute("SELECT id FROM Recipe WHERE name = ?", (name,)).fetchone()
            super().get_connection.commit()
            super().close_db()
            print("Now lets add the Instapot recipe's ingredients.")
            #invokes add_ingredient method from parent class to add ingredients for this recipe
            super().add_ingredient(r_id[0])
        except Exception as x:
            print("Oh boy... An error occurred:", x)

    #this method overwrites the update method in the parent class to include settings and vent_type variables
    def update(self, id, name, preptime, cooktime, difficulty, instructions, settings, vent_type):
        try:
            category = input("Please select a category for the Instapot recipe you are updating: \n1. Appetizer\n2. Salad\n3. Entree\n4. Dessert\n5. Drink\n")
            super().connect()
            super().get_cursor.execute("UPDATE Recipe SET name = ?, preptime = ?, cooktime = ?, difficulty = ?, category_id = ?, instructions = ?, cook_setting = ?, vent_type = ? WHERE id = ?;", (name, preptime, cooktime, difficulty, category, instructions, settings, vent_type, id))
            super().get_connection.commit()
            super().close_db()
            print("Instapot recipe properties updated successfully")
            #print updated version of recipe
            print(self.fetch(recipe_id=id))
            print("\n")
        except Exception as x:
            print("Whoo doggy! An error has occurred:", x)


#-----------------------------------------------------------------------------------------------------------------------
#this is a childclass of the parentclass Recipe.  It includes baking dish specifications and high-altitude adjustments
#not needed in traditional recipes.
class Oven(Recipe):
    def __init__(self):
        super().__init__()

    #this method overwrites Recipe.add to include dish-type and high-altitude adjustment variables
    def add(self, name, preptime, cooktime, difficulty, instructions, dish_type, high_alt_adj):
        try:
            category = input("Please select a category for your baked recipe: \n1. Appetizer\n2. Salad\n3. Entree\n4. Dessert\n5. Drink\n")
            super().connect()
            super().get_cursor.execute("INSERT INTO Recipe(name, preptime, cooktime, difficulty, category_id, instructions, baking_dish, high_alt_adj) VALUES (?,?,?,?,?,?,?,?);", (name, preptime, cooktime, difficulty, category, instructions, dish_type, high_alt_adj))
            r_id = super().get_cursor.execute("SELECT id FROM Recipe WHERE name = ?", (name,)).fetchone()
            super().get_connection.commit()
            super().close_db()
            print("Now lets add the baked recipe's ingredients.")
            #invokes method to add ingredients to recipe
            super().add_ingredient(r_id[0])
        except Exception as x:
            print("Flibberty Gibbets! An error has occurred:", x)

    #this method overwrites Recipe.update to include dish-type and high-altitude adjustment variables
    def update(self, id, name, preptime, cooktime, difficulty, instructions, dish_type, high_alt_adj):
        try:
            category = input("Please select a category for the baked recipe you are updating: \n1. Appetizer\n2. Salad\n3. Entree\n4. Dessert\n5. Drink\n")
            super().connect()
            super().get_cursor.execute("""UPDATE Recipe SET name = ?, preptime = ?, cooktime = ?, difficulty = ?, category_id = ?, instructions = ?, baking_dish = ?, high_alt_adj = ? WHERE id = ?;""", (name, preptime, cooktime, difficulty, category, instructions, dish_type, high_alt_adj, id))
            super().get_connection.commit()
            super().close_db()
            print("Baked recipe properties updated successfully")
            #print updated version of recipe
            print(self.fetch(recipe_id=id))
            print("\n")
        except Exception as x:
            print("Cheese and crackers! An error has occurred:", x)




# print(".oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.\n","                              ....                           \n", "                             ||                              \n", '                         /"""l|\                             \n', "                        /_______\                            \n", "                        |  .-.  |------                      \n", "                         __|L|__| .--.                       \n", "                        _\  \\\\p__`o-o'_                      \n", " ----------------------------------------------------------- \n", " ----------Welcome to Michelle's Recipe Manager!------------ \n", ".oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.")
# print("")



# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
#                               ....
#                              ||
#                          /"""l|\
#                         /_______\
#                         |  .-.  |------
#                          __|L|__| .--.
#                         _\  \\p__`o-o'_
#  -----------------------------------------------------------
#  ----------Welcome to Michelle's Recipe Manager!------------
# .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.



# oven_baked = Oven()
# oven_baked.add("Mom's Cake", "10 minutes", "50 minutes", "Intermediate", "Cream butter and sugar together until completely combined.  Then add eggs and slowly mix.  Sift together flour and other dry ingredients, and then slowly add to batter a bit at a time.  Finally, place in prepared baking dish, bake, and enjoy!  This cake is best without frosting.", "9x13 glass dish", "No adjustment needed")
# oven_baked.add_ingredient(5)
# oven_baked.update(5,"Mom's Cake", "10 minutes", "50 minutes", "Intermediate", "Cream butter and sugar together until completely combined.  Then add eggs and slowly mix.  Sift together flour and other dry ingredients, and then slowly add to batter a bit at a time.  Finally, place in prepared baking dish, bake at 350 degrees for 50 minutes and enjoy!  This cake is best without frosting.", "9x13 glass dish", "No adjustment needed" )
# oven_baked.delete(3)


# recipe_mngr = Recipe()

# recipe_mngr.add("Celestial Bowl", "5 Minutes", "3 Minutes", "Beginner", "Mix ingredients in bowl until everything is fully incorporated.  Then microwave for 2 minutes.  Let cool for 1 minute, and then enjoy!")
# print(recipe_mngr.fetch(3,None))
# print(recipe_mngr.fetch_ing(3))
# recipe_mngr.update(3, "Mama's Oatmeal Bowl", "5 minutes", "3 minutes", "Beginner", "Mix ingredients in bowl until everything is fully incorporated.  Then microwave for 2 minutes.  Let cool for 1 minute, and then enjoy!")

#self, id, name, preptime, cooktime, difficulty, instructions
#recipe_mngr.add_ingredient(3)
# recipe_mngr.delete(3)
#print(recipe_mngr.search_by_ingredient("Water"))
# print(recipe_mngr.search_by_category(3))
# insta_recipe = Instapot()
# insta_recipe.add("Insta Mashed Potatoes", "5 minutes", "5 minutes", "easy", "dice potatoes and place them in instapot with enough water to cover them.  Cook for 2 minutes", "manual setting, on high", "quick vent")
#print(insta_recipe.fetch(4))
# insta_recipe.update(4, "Insta-Taters", "5 minutes", "5 minutes", "easy", "dice potatoes and place them in instapot with enough water to cover them.  Cook for 2 minutes", "manual setting, on high", "quick vent")
