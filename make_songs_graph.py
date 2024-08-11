"""CSC111 Project 2 - Personalized Music Discoveries: Graph Formation Module
===============================

This Python module contains modified graph and vertex classes to represent the connections between albums,
and their genres and characteristics. The graph is formed from a json file that contains information about an album,
as well as the information their reviews provide about them.

Copyright and Usage Information
===============================

This module was made by Shanaya Goel

"""
from __future__ import annotations
import json


class _Vertex:
    """
     A vertex in a song album graph used to represent an album, genre, or characteristic.

    Each vertex item is either an album title, a genre name, or a characteristic. These are all represented as strings.

    Instance Attributes:
        - item: The data stored in this vertex, representing an album, genre or characteristic of a song
        - kind: The type of this vertex: 'album', 'genre or 'characteristic'.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'album', 'genre', 'characteristic'}
    """
    item: str
    kind: str
    neighbours: set[_Vertex]

    def __init__(self, item: str, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'album', 'genre', 'characteristic}
        """
        self.item = item
        self.kind = kind
        self.neighbours = set()


class Graph:
    """
    A graph used to connect song albums to genres and characteristics,
    while also holding scores representing ratings for each song album
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    #     - scores:
    #         A collection of the scores attributed to some vertices(in this program that would be the albums)
    #         Maps album to the average between critic rating and user rating
    _vertices: dict[str, _Vertex]
    scores: dict[str, int]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}
        self.scores = {}

    def add_vertex(self, item: str, kind: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'album', 'genre', 'characteristic'}
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, kind)

    def add_edge(self, item1: str, item2: str) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def adjacent(self, item1: str, item2: str) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: str, kind: str = '') -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', 'album', 'genre', 'characteristic'}


        """
        if item in self._vertices:
            neighbours = self._vertices[item].neighbours
            if kind != '':
                return {n.item for n in neighbours if n.kind == kind}
            else:
                return {n.item for n in neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', 'album', 'genre', 'characteristic'}
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    def get_similarity_list(self, album_verts: list[str], desirable: list[str]) -> dict[str: int]:
        """
        Return how many of the traits in the desirable list are
        connected to each album vertex in the album_verts list(containing the items) in a dictionary.
        This function can be used to take the list of possible albums and attribute them
        to a score of how many of the desired characteristics they contain

        Preconditions:
        - album_verts only contains vertices within self._vertices with kind 'album'
        - desirable only contains vertices within self._vertices with kind 'characteristic'

        >>> lst1 = ["album1", "album2", "album3"]
        >>> lst2 = ["catchy", "melodic", "lyrical"]
        >>> g = Graph()
        >>> g.add_vertex("album1", "album")
        >>> g.add_vertex("album2", "album")
        >>> g.add_vertex("album3", "album")
        >>> g.add_vertex("album4", "album")
        >>> g.add_vertex("catchy", "characteristic")
        >>> g.add_vertex("melodic", "characteristic")
        >>> g.add_vertex("lyrical", "characteristic")
        >>> g.add_vertex("fresh", "characteristic")
        >>> g.add_edge("album1", "catchy")
        >>> g.add_edge("album2", "catchy")
        >>> g.add_edge("album3", "catchy")
        >>> g.add_edge("album3", "lyrical")
        >>> g.add_edge("album1", "fresh")
        >>> dict1 = g.get_similarity_list(lst1, lst2)
        >>> dict1 == {"album1": 1, "album2": 1, "album3": 2}
        True

        """
        album_similarity = {}
        for v in album_verts:
            traits = self.get_neighbours(v, 'characteristic')
            album_similarity[v] = len([t for t in desirable if t in traits])
        return album_similarity


def load_album_graph(file_name: str) -> Graph:
    """Return an album graph corresponding to the given datasets.

    The album graph stores all the information from the album_data file as follows:
    Create one vertex for each album, as well as each genre and characteristic that was associated with an album.
    Edges represent the connection between an album and a characteristic or genre.

    The vertices of the 'album' kind should have a string representing the album name : "[album name] by [artist]"
    The vertices of the 'genre' kind represents a genre.
    The vertices of the 'characteristic' kind represent a characteristic/keyword

    Use the "kind" _Vertex attribute to differentiate between the two vertex types.

    Preconditions:
        - file_name is the path to a json file corresponding to the album data file we provided


    """
    with open(file_name, encoding='utf-8') as f:
        album_data = json.load(f)
        album_graph = Graph()
        for r in album_data:
            if r['artist'] is None:
                artist = 'unknown artist'
            else:
                artist = r['artist']
            if r['title'] is None:
                title = '*unamed album*'
            else:
                title = r['title']
            album_name = title + " by " + artist
            album_graph.add_vertex(album_name, 'album')
            user_rating = r['user_score']
            critic_rating = r['critic_score']

            if user_rating is not None and critic_rating is not None:
                album_graph.scores[album_name] = (int(user_rating) + int(critic_rating)) // 2
            elif user_rating is not None:
                album_graph.scores[album_name] = user_rating
            elif critic_rating is not None:
                album_graph.scores[album_name] = critic_rating
            else:
                album_graph.scores[album_name] = 0

            for g in r['genre']:
                album_graph.add_vertex(g, 'genre')
                album_graph.add_edge(album_name, g)
            for review in r['reviews']:
                for keyword in review['keywords']:
                    album_graph.add_vertex(keyword, 'characteristic')
                    album_graph.add_edge(album_name, keyword)
    return album_graph


if __name__ == '__main__':

    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['json', 'python_ta'],
        'allowed-io': ['load_album_graph'],
        'max-line-length': 120
    })
