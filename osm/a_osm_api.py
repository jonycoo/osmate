from osm.osm_util import Element, Note, ChangeSet
from datetime import *


class OsmApi:

    def get_api_versions(self):
        """
        GET /api/versions

        :returns: supported API versions
        """
        raise NotImplementedError

    def get_api_capabilities(self):
        """
        GET /api/capabilities

        :returns:
        """
        raise NotImplementedError

    def get_permissions(self, auth) -> set:
        """
        current permissions
        Authorisation required
        """
        raise NotImplementedError

    ############################################### CHANGESET #######################################################

    def create_changeset(self, tags: dict, auth) -> int:
        """
        Authorisation required
        :param tags: Dictionary containing additional tags
        :param auth: either OAuth1 object or tuple (username, password)
        :returns: changeset ID
        :raises ParseError:
        """
        raise NotImplementedError

    def get_changeset(self, cid: int, discussion: bool = False) -> ChangeSet:
        """
        A Call to get a changeset optionally with discussion.
        no elements included

        :param cid: changeset ID
        :param discussion: include changeset discussion?
        :returns: dictionary representation of the changeset
        :raises NoneFoundError: no changeset matching this ID
        """
        raise NotImplementedError

    def edit_changeset(self, changeset: ChangeSet, auth):
        """
        Authorisation required

        :param auth: either OAuth1 object or tuple (username, password)
        """
        raise NotImplementedError

    def close_changeset(self, cid: int, auth):
        """
        closes a changeset
        Authorisation required

        :param cid: changeset ID
        :param auth: either OAuth1 object or tuple (username, password)
        :raises NoneFoundError: does not exist
        :raises ConflictError: deleted
        """
        raise NotImplementedError

    def download_changeset(self, cid: int) -> str:
        """
        GET /api/0.6/changeset/#id/download
        """
        raise NotImplementedError

    def get_changesets(self, bbox: tuple = None, user: str = '', time1: datetime = None, time2: datetime = None,
                       is_open: bool = True, is_closed: bool = True, changesets: list = None) -> list:
        """
        returns max 100 changesets matching all provided parameters
        GET /api/0.6/changesets
        parameters by ?/&
        """
        raise NotImplementedError

    def diff_upload(self, cid: int) -> list:
        """
        Authorisation required
        POST /api/0.6/changeset/#id/upload

        :param auth: either OAuth1 object or tuple (username, password)
        """
        raise NotImplementedError

    def comm_changeset(self, cid: int, text: str, auth) -> str:
        """
        Authorisation required
        Add a comment to a changeset. The changeset must be closed.

        :param cid: changeset ID
        :param text: text in new comment
        :param auth: either OAuth1 object or tuple (username, password)
        :raises ValueError: no textfield present
        :raises ConflictError: deleted
        """
        raise NotImplementedError

    def sub_changeset(self, cid: int, auth) -> ChangeSet:
        """
        Subscribes the current authenticated user to changeset discussion
        Authorisation required

        :param cid: changeset ID
        :param auth: either OAuth1 object or tuple (username, password)
        :raises ConflictError: already subscribed
        """
        raise NotImplementedError

    def unsub_changeset(self, cid: int, auth) -> ChangeSet:
        """
        Unsubscribe the current authenticated user from changeset discussion
        Authorisation required

        :param cid: changeset ID
        :param auth: either OAuth1 object or tuple (username, password)
        :raises NoneFoundError: is not subscribed
        """
        raise NotImplementedError

    ############################################## ELEMENT #########################################################

    def create_element(self, elem: Element, cid: int, auth) -> int:
        """
        creates new element of specified type
        Authorisation required

        :param elem: element to get created
        :param cid: open changeset ID
        :param auth: either OAuth1 object or tuple (username, password)
        :returns: Element ID
        :raises NoneFoundError:
            When there are errors parsing the XML -> ParseError
            When a changeset ID is missing (unfortunately the error messages are not consistent)
            When a node is outside the world
            When there are too many nodes for a way
        :raises ConflictError:
            When changeset already closed
            When changeset creator and element creator different
        :raises ParseError: When a way/relation has nodes that do not exist or are not visible
        """
        raise NotImplementedError

    def get_element(self, etype: str, eid: int) -> Element:
        """
        :returns: Element containing all available data.
        :raises NoneFoundError: No Element with such id
        :raises LockupError: Deleted Element
        """
        raise NotImplementedError

    def edit_element(self, elem: Element, cid: int, auth) -> int:
        """
        Authorisation required

        :param elem: changed element to get uploaded
        :param cid: open changeset id
        :param auth: either OAuth1 object or tuple (username, password)
        :returns: New version Number
        :raises ValueError:
            When there are errors parsing the XML
            When a changeset ID is missing
            When a node is outside the world
            When there are too many nodes for a way
            When the version of the provided element does not match the current database version of the element
        :raises NoneFoundError: Element ID not found
        :raises ConflictError:
            When changeset already closed
            When changeset creator and element creator different
        :raises ParseError: When a way/relation has nodes that do not exist or are not visible
        """
        raise NotImplementedError

    def delete_element(self, elem: Element, cid: int, auth) -> int:
        """
        Authorisation required

        :param elem: changed element to get deleted
        :param cid: open changeset id
        :param auth: either OAuth1 object or tuple (username, password)
        :returns: new version number
        :raises ValueError:
            When there are errors parsing the XML
            When a changeset ID is missing
            When a node is outside the world
            When there are too many nodes for a way
            When the version of the provided element does not match the current database version of the element
        :raises ConflictError:
            When changeset already closed
            When changeset creator and element creator different
        :raises LookupError: deleted
        :raises ParseError:
            When node is still part of way/relation
            When way is still part of relation
            When relation is still part of another relation
        """
        raise NotImplementedError

    def history_element(self, etype: str, eid: int) -> list:
        """
        Returns all available previous versions of the element
        GET /api/0.6/[node|way|relation]/#id/history
        """
        raise NotImplementedError

    def history_version_element(self, etype: str, eid: int, version: int = None) -> Element:
        """
        Return specified version of element
        GET /api/0.6/[node|way|relation]/#id/#version
        """
        raise NotImplementedError

    def get_elements(self, etype: str, eids: list) -> list:
        """
        :note: returns only elements of the same type
        :returns: multiple elements as specified in the list of eid
        :param etype: element type one of [node, way, relation]
        :param eids: list of eid
        """
        raise NotImplementedError

    def get_relation_of_element(self, etype: str, eid: int) -> list:
        """
        :returns: direct relations and ways connected to element
        :param etype: element type one of [node, way, relation]
        :param eid: element ID
        """
        raise NotImplementedError

    def get_ways_of_node(self, eid: int) -> list:
        """
        use only on node elements
        :returns: ways directly using this node
        :raises NoneFoundError: no connected ways found
        """
        raise NotImplementedError

    def get_element_bbox(self, bbox: tuple) -> list:
        """
        :returns: all Elements with minimum one Node within this BoundingBox
        :raise NoneFoundError: either none or over 50.000 element are found
        """
        raise NotImplementedError

    def get_full_element(self, etype: str, eid: int) -> list:
        """
        GET /api/0.6/[way|relation]/#id/full
        """

    # reduction purposefully left out (only for moderators)

    ################################################## GPX ########################################################

    def get_gpx_bbox(self, bbox: tuple, page: int) -> dict:
        """
        returns 5000GPS trackpoints max, increase page for any additional 5000

        :param bbox: (minlon, minlat, maxlon, maxlat)
        :param page: 5000 trackpoints are returned each page
        :returns: max 5000 trackpoints within bbox, format GPX Version 1.0
        """
        raise NotImplementedError

    def upload_gpx(self, trace: str, name: str, description: str, tags: set, auth,
                   public: bool = True, visibility: str = 'trackable') -> int:
        """
        uploads gpx trace
        Authorisation required


        :param trace: gpx trace file string
        :param description: gpx description
        :param name: file name on osm
        :param tags: additional tags mappingtour, etc
        :param auth: either OAuth1 object or tuple (username, password)
        :param public: True for public tracks else False
        :param visibility: one of [private, public, trackable, identifiable]
            more https://wiki.openstreetmap.org/wiki/Visibility_of_GPS_traces
        :returns: gpx_id
        """
        raise NotImplementedError

    def update_gpx(self, tid: int, trace: str, description: str, tags: set, auth,
                   public: bool = True, visibility: str = 'trackable'):
        """
        updates gpx trace
        Authorisation required

        :param tid: uploaded trace id
        :param trace: gpx trace as string
        :param description: gpx description
        :param tags: additional tags mappingtour, etc
        :param auth: either OAuth1 object or tuple (username, password)
        :param public: True for public tracks else False
        :param visibility: one of [private, public, trackable, identifiable]
            more https://wiki.openstreetmap.org/wiki/Visibility_of_GPS_traces
        :returns: None
        """
        raise NotImplementedError

    def delete_gpx(self, gpx_id: int, auth):
        """
        Authorisation required

        :param gpx_id: id identifying the gpx file on the server
        :param auth: either OAuth1 object or tuple (username, password)
        """
        raise NotImplementedError

    def get_meta_gpx(self, gpx_id: int) -> dict:
        """
        GET /api/0.6/gpx/#id/details

        :param gpx_id: id identifying the gpx file as string
        :returns: dictionary representing the metadata
        """
        raise NotImplementedError

    def get_gpx(self, gpx_id: int) -> str:
        """

        :param gpx_id: id identifying the gpx file on the server
        :returns: gpx file as string
        """
        raise NotImplementedError

    def get_own_gpx(self, auth) -> list:
        """
        Authorisation required

        :param auth: either OAuth1 object or tuple (username, password)
        :returns: list of dictionary representing the metadata
        """
        raise NotImplementedError

    ################################################# USER ######################################################

    def get_user(self, uid: int) -> dict:
        """
        :param uid: user id
        :returns: dictionary with user detail
        """
        raise NotImplementedError

    def get_users(self, uids: list) -> list:
        """
        :param uids: uid in a list
        :returns: list of dictionary with user detail
        """
        raise NotImplementedError

    def get_current_user(self, auth):
        """
        Authorisation required

        :param auth: either OAuth1 object or tuple (username, password)
        :returns: dictionary with user detail
        """
        raise NotImplementedError

    def get_own_preferences(self, auth) -> dict:
        """
        Authorisation required

        GET /api/0.6/user/preferences

        :param auth: either OAuth1 object or tuple (username, password)
        :returns: dictionary with preferences
        """
        raise NotImplementedError

    def update_own_preferences(self, pref: dict, auth):
        """
        Authorisation required

        PUT /api/0.6/user/preferences

        :param auth: either OAuth1 object or tuple (username, password)
        :param pref: dictionary with preferences
        """
        raise NotImplementedError

    def get_own_preference(self, key: str, auth) -> str:
        """
        Authorisation required

        GET /api/0.6/user/preferences/<your_key>

        :param auth: either OAuth1 object or tuple (username, password)
        :param key: key of preference
        :returns: value
        """
        raise NotImplementedError

    def set_own_preference(self, key: str, value: str, auth):
        """
        Authorisation required

        PUT /api/0.6/user/preferences/<your_key>

        :param key: key of preference
        :param value: new value
        :param auth: either OAuth1 object or tuple (username, password)
        """
        raise NotImplementedError

    def delete_own_preference(self, key: str, auth):
        """
        Authorisation required

        DELETE /api/0.6/user/preferences/[your_key]

        :param key: key of preference
        :param auth: either OAuth1 object or tuple (username, password)
        """

    ################################################# NOTE ######################################################

    def get_notes_bbox(self, bbox: tuple, limit: int = 100, closed: int = 7) -> list:
        """
        :param bbox: (lonmin, latmin, lonmax, latmax)
        :param limit: 0-1000
        :param closed: max days closed -1=all, 0=only_open
        :returns: list of Notes
        :raises ValueError: HTTP 400 BAD REQUEST
            When any of the limits are crossed
        """
        raise NotImplementedError

    def get_note(self, nid: int) -> Note:
        """
        :param nid: note id
        :return: the identified Note
        :raises NoneFoundError: HTTP 404 NOT FOUND no note with this id
        """
        raise NotImplementedError

    def create_note(self, text: str, lat: float, lon: float, auth) -> Note:
        """
        Authorisation optional

        :param text: Note Text
        :param lat: latitude
        :param lon: longitude
        :param auth: either OAuth1 object or tuple (username, password)
        :returns: Note ID
        :raises ValueError: No text field
        """
        raise NotImplementedError

    def comment_note(self, nid: int, text: str, auth) -> Note:
        """
        Authorisation required

        :param nid: Note ID
        :param text: Text
        :param auth: either OAuth1 object or tuple (username, password)
        :returns: the Note itself
        :raises ValueError: HTTP 400 BAD REQUEST No Textfield
        :raises NoneFoundError: HTTP 404 NOT FOUND
        :raises ConflictError: HTTP 409 CONFLICT closed Note
        """
        raise NotImplementedError

    def close_note(self, nid: int, text: str, auth) -> Note:
        """
        Authorisation required

        :param nid: Note ID
        :param text: Closing comment
        :param auth: either OAuth1 object or tuple (username, password)
        :returns: the Note itself
        :raises NoneFoundError: HTTP 404 NOT FOUND
        :raises MethodError: HTTP 405 METHOD NOT ALLOWED
        :raises ConflictError: HTTP 409 CONFLICT closed Note
        """
        raise NotImplementedError

    def reopen_note(self, nid: int, text: str, auth):
        """
        Authorisation required

        :param nid: Note ID
        :param text: Text
        :param auth: either OAuth1 object or tuple (username, password)
        :returns: the Note itself
        :raises NoneFoundError: HTTP 404 NOT FOUND
        :raises MethodError: HTTP 405 METHOD NOT ALLOWED
        :raises ConflictError: HTTP 409 CONFLICT closed Note
        :raises LookupError: HTTP 410 GONE deleted Note
        """
        raise NotImplementedError

    def search_note(self, text: str, limit: int = 100, closed: int = 7, username: str = None, user: int = None,
                    start: datetime = None, end: datetime = None,
                    sort: str = 'updated_at', order: str = 'newest') -> list:
        """
        Authorisation required
        GET /api/0.6/notes/search?q=<SearchTerm>&limit=&closed=&username=&user=&from=&to=&sort=&order=

        :param text: <free text>
        :param limit: 0-1000
        :param closed: max days closed -1=all, 0=only_open
        :param username: username
        :param user: User ID
        :param start: from earliest date
        :param end: to newer date default: today
        :param sort: created_at or updated_at
        :param order: oldest or newest
        :returns: list of Notes
        :raises ValueError: HTTP 400 BAD REQUEST
            When any of the limits are crossed
        """
        raise NotImplementedError

    def rss_notes(self, bbox) -> str:
        """
        GET /api/0.6/notes/feed?bbox=left,bottom,right,top

        :param bbox: (lonmin, latmin, lonmax, latmax)
        :return:
        """
        raise NotImplementedError
