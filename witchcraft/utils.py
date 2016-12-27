import re


def normalize(name):
    """Normalize an artist or track name.

    Parameters
    ----------
    name : str
        The raw name.

    Returns
    -------
    normalized : str
        The normalized name.
    """
    name = name.lower().strip()
    name = re.sub(r"[.()&',]", '', name)  # drop special chars
    name = re.sub(r'[\s_]', '-', name)  # normalize whitespace
    name = re.sub(r'-+', '-', name)  # fold hyphens
    return name


def normalize_beatport(name):
    """Normalize a track name when we know that it comes from beatport.

    Parameters
    ----------
    name : str
        The raw name.

    Returns
    -------
    normalized : str
        The normalized name.

    Notes
    -----
    This functions stripts the '(Original Mix)' suffix.

    """
    name = name.rsplit(' (Original Mix)')
    return normalize(name)


def normalize_genre(name):
    """Normalize a genre name. We try to fold common spellings of the same
    genre together, for example, 'drum & bass' == 'drum-and-bass'.

    Parameters
    ----------
    name : str
        The raw name.

    Returns
    -------
    normalized : str
        The normalized name.

    Notes
    -----
    We prefer 'drum-and-bass' to 'drum-&-bass' because we never want to need
    to escape a query.
    """
    name = name.lower()
    try:
        return _genre_map[name]
    except KeyError:
        return normalize(name)


# map for normalizing genres
_genre_map = {
    'drum & bass': 'dnb',
    'drum and bass': 'dnb',
    'd and b': 'dnb',
}


def normalize_track_number(number):
    """Normalize the track number.

    Parameters
    ----------
    number : str
        The number as a string


    Returns
    -------
    normalized : int
        The track number as an int.

    Notes
    -----
    Some files will use a tag like ``n/m`` where ``n`` is the tracknumber and
    ``m`` is total number of tracks on the album.
    """
    number = number.split('/', 1)[0]
    return int(number)


def normalize_artist(artist):
    """Normalize an artist name.

    Parameters
    ----------
    artist : str
        The artist name as a string.

    Returns
    -------
    normalized : iterable[str]
        The artist names parsed out of the string.

    Notes
    -----
    Some files will use one tag with comma delimited artists instead of a list
    of artist tags.
    """
    return map(normalize, artist.split(','))
