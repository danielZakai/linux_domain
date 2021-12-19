import sys
import os


def organize_dictionary(inp):
    """
    * Function name: organize_dictionary
    * What the function does:
    * Takes the original input text and organizes it into a dictionary of all the movies
    * Keyword argument: The input text file
    * Return: The organized dictionary
    """
    # initialize movie dictionary
    movies = {}
    # split the lines by movies
    for line in inp:
        inputed_line = line.rstrip("\n").split(", ")
        # check if the movie is in the dictionary
        for i in range(1, len(inputed_line)):
            # if it is
            if inputed_line[i] in movies:
                # add the actor to the movie
                movies[inputed_line[i]].add(inputed_line[0])
            else:
                # if it is not, intialize a set of actors
                set_of_actors = set()
                # add the the first actor to the set of actors
                set_of_actors.add(inputed_line[0])
                # the movie in the i'th place in the dictionary is equal to the first actor
                movies[inputed_line[i]] = set_of_actors
    return movies


def main_menu(movies):
    """
    * Function name: main_menu
    * What the function does: runs the main menu of the program- takes the input of the users and
    * calls the appropriate function
    * Keyword argument: The movies dictionary
    * Return: -
    """
    while True:
        print("Please select an option:")
        print("1) Query by movies")
        print("2) Query by actor")
        print("3) Insert a new movie")
        print("4) Save and Exit")
        print("5) Exit")
        option = input()
        # first option
        if option == '1':
            query_by_movies(movies)
        if option == '2':
            query_by_actor(movies)
        if option == '3':
            insert_new_movie(movies)
        if option == '4':
            save_file(movies)
            exit(0)
        if option == '5':
            exit(0)
    # end of function


def query_by_movies(movies):
    """
    * Function name: query_by_movies
    * What the function does: Takes the user input of 2 movies and either an &, | or ^ sign
    * if the user entered & - print all the actors who acted in both the first and the second movie
    * if the user entered | - print all the actors who acted in either first or the second movie
    * if the user entered ^ - print all the actors who acted in only one of the movies
    * Keyword argument: The movies dictionary
    * Return: -
    """
    print("Please select two movies and an operator(&,|,^) separated with ',':")
    option = input()
    new_input = [new_input.strip() for new_input in option.split(',')]
    if new_input[0] not in movies or new_input[1] not in movies:
        print("Error")
        return
    if new_input[2] is not '&' and new_input[2] is not '|' and new_input[2] is not '^':
        print("Error")
        return
    if len(new_input)<3:
        print("Error")
        return
    if new_input[2] == '&':
        common_actors = movies[new_input[1]].intersection(movies[new_input[0]])
        if common_actors == set():
            print("There are no actors in this group")
            return
        print(', '.join(sorted(common_actors)))
    if new_input[2] == '|':
        all_actors = movies[new_input[1]].union(movies[new_input[0]])
        if all_actors == set():
            print("There are no actors in this group")
            return
        print(', '.join(sorted(all_actors)))
    if new_input[2] == '^':
        exclusive_actors = movies[new_input[1]].symmetric_difference(movies[new_input[0]])
        if exclusive_actors == set():
            print("There are no actors in this group")
            return
        print(', '.join(sorted(exclusive_actors)))
        # end of function


def query_by_actor(movies):
    """
    * Function name: query_by_actor
    * What the function does: Takes the user input an actor and prints all the co actors of that actor
    * Keyword argument: The movies dictionary
    * Return: -
    """
    print("Please select an actor:")
    actor = input()
    movie_names = []
    all_common_actors = set()
    actor_exists_flag = False
    # iterate over all the movies and see which movies the inputted actor was in
    for movie, actors in movies.items():
        # if the actor is found in the movie
        if actor in actors:
            # create a new set with all the movies he preformed in
            movie_names.append(movie)
            actor_exists_flag = True
    if not actor_exists_flag:
        print("Error")
        return
    # check the current set with the original dictionary to see which moves are in both
    for name in movie_names:
        # take all of the actors who worked with the inputted actor
        all_common_actors.update(movies[name])
    # if there is at least one common actor
    if len(all_common_actors) != 0:
        # organize our common actors
        final_common_actors = sorted(all_common_actors)
        # remove the users actor input
        for current_actor in all_common_actors:
            if current_actor == actor:
                final_common_actors.remove(current_actor)
        print(', '.join(final_common_actors))
    # if there is not
    else:
        print("There are no actors in this group")
    # end of function


def insert_new_movie(movies):
    """
    * Function name: insert_new_movie
    * What the function does: Takes the user input of either a new movie with its actors or a movie already
    * in the dictionary with more actors. If it is a new movie add it to the dictionary, if it is a movie
    * already in the list than add the actors to the actor list of the movie
    * Keyword argument: The movies dictionary
    * Return: -
    """
    print("Please insert a new movie:")
    # split the input by commas and spaces
    new_movie = input().strip().split(", ")
    # loop over the new input and strip each space
    for i in range(0, len(new_movie)):
        new_movie[i] = new_movie[i].strip()
        # if the input length is too short- it is an error
    if len(new_movie) < 2:
        print("Error")
        return
    # if the movie input is already in our movie dictionary
    if new_movie[0] in movies:
        # add the actors to the existing movie
        for i in range(1, len(new_movie)):
            movies[new_movie[0]].add(new_movie[i])
    # if not
    else:
        # create a set for the new actors in the new movie
        set_of_new_actors = set()
        for i in range(1, len(new_movie)):
            # add the actors in the new movie to the set
            set_of_new_actors.add(new_movie[i])
            # add the new movie with the actors to the dictionary
            movies[new_movie[0]] = set_of_new_actors


def save_file(movies):
    """
    * Function name: save_file
    * What the function does: Organizes a new dictionary with the actors and there movies and sends it to an output
    * file
    * Keyword argument: The movies dictionary
    * Return: -
    """
    # set a new dictionary for converting back to the right order
    organized_by_actor = {}
    os.chmod('out.txt', 0o777)
    # open the output file
    output_file = open(sys.argv[2], "w+")
    # loop over our current dictionary
    for movie, actors in movies.items():
        # check if the actor is in our new dictionary
        for actor in actors:
            # if it is
            if actor in organized_by_actor:
                # add the movie we are at to the current actor
                organized_by_actor[actor].append(movie)
            # if not
            else:
                # make a new list
                list_of_organized_movies = list()
                # add our current movie to the list
                list_of_organized_movies.append(movie)
                # our new dictionary is the our current actor with all the movies the actor acted in
                organized_by_actor[actor] = list_of_organized_movies
    # make a new list that will sort the dictionary in the correct order
    actor_list = sorted(organized_by_actor)
    # loop over our new list and print each line out to an output file
    for actor in actor_list:
        output_file.write(actor + ', ' + str(sorted(organized_by_actor[actor])).strip('[]').replace("'", '') + "\n")
    # close the output file
    output_file.close()
    # end of function


def main():
    """
    * Function name: main
    * What the function does: Opens the input text and call the main menu function which the runs program
    * Keyword argument: -
    * Return: -
     """
    # open the input file
    inp = open(sys.argv[1], "r")
    print("Processing...")
    # movies is our dictionary
    movies = organize_dictionary(inp)
    # call the main menu function
    main_menu(movies)
    #close the input file
    inp.close()
    # end of function


if __name__ == '__main__':
  main()
