import json
import math
from datetime import datetime
import dateutil.parser

OSM_URL = 'https://master.apis.dev.openstreetmap.org'

class Element:
    def __init__(self, eid: int, version: int, changeset: int,
                 user: str, uid: int, created: str, visible: bool, tags: dict):
        """

        :param eid:
        :param tags:
        """
        self._id = eid
        self.tags = tags or {}
        self.version = version
        self.changeset = changeset
        self.user = user
        self.uid = uid
        self.created = created
        self.visible = visible
        self.e_type = 'element'

    def __repr__(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__)

    def __str__(self):
        if self.created:
            rt = '{} {}\ncreated: {}\nversion: {}\nvisible: {}\nchangeset: {}\n{} {}\n ---- \n'\
                .format(self.e_type, self._id, self.created, self.version,
                        self.visible, self.changeset, self.user, self.uid)
        else:
            rt = 'type: {}\n ---- \n'.format(self.e_type)
        return rt.join(map('\n'.join, self.tags))

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self.e_type


class MicroElem:
    def __init__(self, eid, e_type, tags: dict = None):
        self.eid = eid
        self.e_type = e_type
        self.tags = tags or {}

    def __str__(self):
        return self.e_type + str(self.eid)


class Node(Element):
    def __init__(self, eid: int, lat: float, lon: float, version: int, changeset: int,
                 user: str, uid: int, created: str, visible: bool, tags: dict):
        super().__init__(eid, version, changeset, user, uid, created, visible, tags)
        self.lat = lat
        self.lon = lon
        self.e_type = 'node'

    def __str__(self):
        rt = super().__str__()
        return rt + '\nloc: {}, {}'.format(self.lat, self.lon)


class Way(Element):
    def __init__(self, eid: int, nodes: list, version: int, changeset: int,
                 user: str, uid: int, created: str, visible: bool, tags: dict):
        super().__init__(eid, version, changeset, user, uid, created, visible, tags)
        self.nodes = nodes
        self.e_type = 'way'

    def __str__(self):
        rt = super().__str__()
        return rt + '\nnode_count: {}'.format(len(self.nodes))



class Relation(Element):
    def __init__(self, eid: int, members: list, version: int, changeset: int,
                 user: str, uid: int, created: str, visible: bool, tags: dict):
        super().__init__(eid, version, changeset, user, uid, created, visible, tags)
        self.members = members
        self.e_type = 'relation'

    def __str__(self):
        rt = super().__str__()
        return rt + '\nmember_count: {}'.format(len(self.members))


class Comment:
    def __init__(self, text: str, uid: int, username: str, created: datetime, action: str = None):
        self.text = text
        self._id = uid
        self.user = username
        self.created = created
        self.action = action

    def __repr__(self):
        return json.dumps(self.__dict__)

    @property
    def id(self):
        return self._id


class Note:
    def __init__(self, nid: int, lat: float, lon: float, created: str, is_open: bool, comments: list):
        self._id = nid
        self.lat = lat
        self.lon = lon
        try:
            dateutil.parser.parse(created)
            self._created = created
        except ValueError:
            self._created = None
        # todo date_closed
        self._open = is_open
        self._comments = comments

    def __repr__(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__)

    @property
    def created(self) -> datetime:
        if self._created:
            return dateutil.parser.parse(self._created)
        else:
            return None

    @property
    def id(self):
        return self._id

    @property
    def location(self):
        return self.lat, self.lon


class Trace:
    def __init__(self, tid: int, gpx: str, filename: str, username: str, time: str,
                 desc: str = None, tags: set = None, visibility: str = 'trackable'):
        self._tid = tid
        self.gpx = gpx
        self.name = filename
        self._username = username
        self._timestamp = time
        self.desc = desc or 'no Description'
        self.tags = tags or []
        self.visibility = visibility

    def __repr__(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return self.name

    @staticmethod
    def url(osm_user, tid):
        return OSM_URL + '/user/' + osm_user + '/traces/' + tid


class ChangeSet:
    def __init__(self, cid: int, username: str, uid: int, created: datetime, is_open: bool, bbox: tuple,
                 closed: datetime = None, tags: dict = None, comments: list = None):
        self._id = cid
        self._user = username
        self._uid = uid
        self._created = created
        self.open = is_open
        self.maxlon = bbox[0] or None
        self.maxlat = bbox[1] or None
        self.minlon = bbox[2] or None
        self.minlan = bbox[3] or None
        self.closed = closed
        self.tags = tags or {}
        self.comments = comments or []

    def __repr__(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__)

    @property
    def id(self):
        return self._id

    @property
    def open_comment(self):
        try:
            return self.tags['comment']
        except KeyError:
            return None

    @property
    def bbox(self):
        return self.maxlon, self.maxlat, self.minlon, self.minlan


def create_bbox(lat: float, lon: float, rad: int):
    """
    creates a Geo Bounding box with lat, lon as center

    :param lat: latitude
    :param lon: longitude
    :param rad: radius in meters
    """

    EARTH_RAD = float(6378000)
    lat_d = (math.asin(float(rad) / (EARTH_RAD * math.cos(math.pi * lat / 180)))) * 180 / math.pi
    lon_d = (math.asin(float(rad) / EARTH_RAD)) * 180 / math.pi

    dec = 8

    max_lat = round(lat + lat_d, dec)
    min_lat = round(lat - lat_d, dec)
    max_lon = round(lon + lon_d, dec)
    min_lon = round(lon - lon_d, dec)

    return min_lon, min_lat, max_lon, max_lat
