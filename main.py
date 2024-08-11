"""CSC111 Project 2 - TODO: Make the docstring

Instructions (READ THIS FIRST!)
===============================

This Python module contains the main function that outputs a list of ten albums according to the genre and characteristics the user inputs.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
# Import necessary functions and classes from graph_module
from make_songs_graph import load_album_graph


def main():
    """Run the main program to recommend albums based on user preferences.

    This program interacts with the user to get their preferred genre and characteristics in music.
    It then recommends the top ten albums that match both the genre and characteristic preferences provided by the user.
    """

    # Load album data into the graph from a JSON file
    album_graph = load_album_graph("album_data.json")

    # Interact with the user to get their preferences
    print("Welcome to the Album Recommender!")
    print("Type 'end' at any time to stop.")

    while True:
        genre_preference = input("\nWhat genres do you like to listen to? ")
        if genre_preference.lower() == 'end':
            break
        characteristics = []

        # Input characteristics until 'end' is entered
        while True:
            characteristic = input("Enter a characteristic (or 'end' to stop): ")
            if characteristic.lower() == 'end':
                break
            characteristics.append(characteristic)

        if not characteristics:
            print("You must enter at least one characteristic.")
            continue

        # Get all albums and desirable characteristics from the graph
        all_albums = album_graph.get_neighbours(genre_preference.strip(), kind='album')
        desirable_characteristics = [c for c in characteristics if
                                     c in album_graph.get_all_vertices(kind='characteristic')]

        if not all_albums:
            print("No albums found in the graph. Please check your data.")
            break

        if not desirable_characteristics:
            print("No desirable characteristics found in the graph. Please try again.")
            continue

        # Calculate the similarity between albums and desirable characteristics
        similarity_scores = album_graph.get_similarity_list(all_albums, desirable_characteristics)

        # Sort albums based on their similarity scores
        sorted_albums = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

        # Get the top ten albums
        top_ten_albums = [album for album, _ in sorted_albums[:10]]

        if not top_ten_albums:
            print("No albums found for the given characteristics. Please try again.")
        else:
            print("Top Ten Albums:")
            for album in top_ten_albums:
                print("-", album)
        break

    print("Thank you for using the Album Recommender!")


if __name__ == "__main__":
    main()
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all('main.py', config={
        'max-line-length': 120,
        'extra-imports': ['json', 'python_ta'],
        'allowed-io': ['load_album_graph']
    })
