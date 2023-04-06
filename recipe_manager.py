import recipe_functions as rf

#prints ASCII art of house on a doily and name of program
print(".oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.\n","                              ....                           \n", "                             ||                              \n", '                         /"""l|\                             \n', "                        /_______\                            \n", "                        |  .-.  |------                      \n", "                         __|L|__| .--.                       \n", "                        _\  \\\\p__`o-o'_                      \n", " ----------------------------------------------------------- \n", " ----------Welcome to Michelle's Recipe Manager!------------ \n", ".oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.\n")
try:
    while True:
        #prints a menu of options for user to choose from
        print("Menu of options:")
        print("1. See all recipes\n2. Search for recipe by category\n3. Search for recipe by ingredient\n4. View a recipe\n5. Add a recipe\n6. Update a recipe\n7. Delete a recipe\n8. Exit")
        option = input("Please enter the number of the option you would like to select: ")
        #instantiates objects of each recipe type
        recipe = rf.Recipe()
        insta_recipe = rf.Instapot()
        baked_recipe = rf.Oven()

        if option == "1":  #See all recipes
            all_rec = recipe.fetch()
            #print(rec,"\n")
            for item in all_rec:
                print(item)
            print("--End of List--\n")

        elif option == "2":  #Search for recipe by category
            cat = input("Please select the category you would like to search by: \n1. Appetizer\n2. Salad\n3. Entree\n4. Dessert\n5. Drink\n")
            rec_by_cat = recipe.search_by_category(cat)
            for recipe in rec_by_cat:
                print(recipe)
            print("--End of List--\n")

        elif option == "3":  #Search for recipe by ingredient
            ing = input("Please enter the ingredient you would like to search by: ")
            rec_by_ing = recipe.search_by_ingredient(ing)
            for item in rec_by_ing:
                print(item)
            print("--End of List--\n")

        elif option == "4":  #View a recipe
            rec_id = input("Please enter the id of the recipe you would like to see: ")
            print("\nIngredients:")
            view_ing = recipe.fetch_ing(rec_id)
            print(view_ing,"\n")
            print("Recipe Details:")
            view_rec = recipe.fetch(rec_id)
            print(view_rec,"\n")

        elif option == "5":  #Add a recipe
            #user's input instructs which recipe object type to use
            rec_type = input("Enter whether this is a regular, instapot, or oven-baked recipe:").lower()
            if rec_type == "regular":
                rname = input("Enter recipe name: ").lower()
                rprep = input("Enter prep-time: ")
                rcook = input("Enter cook-time: ")
                rdiff = input("Choose recipe difficulty (easy, intermediate, advanced): ").lower()
                rinstruct = input("Enter recipe instructions: ")
                recipe.add(rname, rprep, rcook, rdiff, rinstruct)

            elif rec_type == "instapot":
                rname = input("Enter recipe name: ").lower()
                rprep = input("Enter prep-time: ")
                rcook = input("Enter cook-time: ")
                rdiff = input("Choose recipe difficulty (easy, intermediate, advanced): ").lower()
                rinstruct = input("Enter recipe instructions: ")
                rsett = input("Enter Instapot setting(s): ")
                rvent = input("Enter Instapot venting method: ")
                insta_recipe.add(rname, rprep, rcook, rdiff, rinstruct, rsett, rvent)

            elif rec_type == "oven-baked":
                rname = input("Enter recipe name: ").lower()
                rprep = input("Enter prep-time: ")
                rcook = input("Enter cook-time: ")
                rdiff = input("Choose recipe difficulty (easy, intermediate, advanced): ").lower()
                rinstruct = input("Enter recipe instructions: ")
                rdish = input("Enter baking dish to be used: ")
                radj = input("Enter any high-altitude adjustments to recipe: ")
                baked_recipe.add(rname, rprep, rcook, rdiff, rinstruct, rdish, radj)

            else:
                print("Invalid entry.  Try again")

        elif option == "6":  #Update a recipe
            update_id = input("Enter id of recipe you want to update: ")
            rec_type = input("Enter whether this is a regular, instapot, or oven-baked recipe:").lower()
            if rec_type == "regular":
                rname = input("Enter recipe name: ").lower()
                rprep = input("Enter prep-time: ")
                rcook = input("Enter cook-time: ")
                rdiff = input("Choose recipe difficulty (easy, intermediate, advanced): ").lower()
                rinstruct = input("Enter recipe instructions: ")
                recipe.update(update_id,rname, rprep, rcook, rdiff, rinstruct)

            elif rec_type == "instapot":
                rname = input("Enter recipe name: ").lower()
                rprep = input("Enter prep-time: ")
                rcook = input("Enter cook-time: ")
                rdiff = input("Choose recipe difficulty (easy, intermediate, advanced): ").lower()
                rinstruct = input("Enter recipe instructions: ")
                rsett = input("Enter Instapot setting(s): ")
                rvent = input("Enter Instapot venting method: ")
                insta_recipe.update(update_id,rname, rprep, rcook, rdiff, rinstruct, rsett, rvent)

            elif rec_type == "oven-baked":
                rname = input("Enter recipe name: ").lower()
                rprep = input("Enter prep-time: ")
                rcook = input("Enter cook-time: ")
                rdiff = input("Choose recipe difficulty (easy, intermediate, advanced): ").lower()
                rinstruct = input("Enter recipe instructions: ")
                rdish = input("Enter baking dish to be used: ")
                radj = input("Enter any high-altitude adjustments to recipe: ")
                baked_recipe.update(update_id,rname, rprep, rcook, rdiff, rinstruct, rdish, radj)

            else:
                print("Invalid entry.  Try again")

            #asks user if ingredients also need to be updated.  If yes, original recipe ingredients are deleted from
            #the db to prevent messiness, and updated ingredients are added as new ingredients
            update_ing = input("Do you need to update ingredients for this recipe? Yes or No: ").lower()
            if update_ing == "no":
                print("Great. Thanks! I'll take you back to the main menu.")
            else:
                recipe.delete_ing(update_id)
                recipe.add_ingredient(update_id)

        elif option == "7":  #Delete a recipe
            del_id = input("Enter id of recipe you want to delete: ")
            #verify user input the correct recipe_id before deleting respective recipe
            verify = input(f"You entered recipe id {del_id}.  Are you sure you want to delete that recipe? Yes or No: ").lower()
            if verify == "no":
                print("Okay.  I'll take you back to the main menu.\n")
            elif verify == "yes":
                recipe.delete(del_id)
            else:
                print("incorrect input. Try again.\n")

        elif option == "8" or option.lower() == "exit":
            break
        else:
            print("\nInvalid entry.  Please enter a number for the option you would like, or type exit.\n")
except Exception as x:
    print("An error occurred:", x)
