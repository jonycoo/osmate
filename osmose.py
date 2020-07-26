'''
Documentation, License etc.

@package osmate
'''

import logging
import requests
import json
from operator import itemgetter
from osm import osm_util
from ee_osmose import NoneFoundError

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

URL = 'http://osmose.openstreetmap.fr/en/api/0.3'
lang = 'en'


class Issue:
    """
        represents an Issue at Open Street Map
    """

    def __init__(self, lat: float, lon: float, e_id: str, title: str,
                 subtitle: str, elems: list, bbox=None):
        """
            Attributes
            ----------
            lat: float
                Latitude
            lon: float
                Longitude
            e_id: str
                error_id from issue provider
            title: str
                Issue title
            subtitle: str
                subtitle

        """

        self.lat = float(lat)
        self.lon = float(lon)
        self.id = e_id
        self.title = title
        self.subtitle = subtitle
        self.elems = elems
        self.bbox = bbox or (0.0, 0.0, 0.0, 0.0)

    @property
    def loc(self) -> tuple:
        """ location (lat, lon)"""
        return self.lat, self.lon

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __str__(self):
        return '"{}" Issue at: {} , elems: {} '\
            .format(self.title, self.loc, [str(elem) for elem in self.elems])

    def osm_url(self):
        return "https://osm.org/#map=18/{}/{}&layers=ND".format(self.lat, self.lon)

    def desc_url(self):
        return "http://osmose.openstreetmap.fr/en/error/" + self.id


def get_issues_user(user: str) -> list:  # future allows arbitrary arguments specifying country, etc.
    """
        searches for Issues of whom the user is the last editor

        Attributes
        ----------
        user : str
            osm username

        Returns
        -------
        list[Issue]
            up to 50 Issues found there.

        Raises
        ------
        NoneFoundError
    """

    logger.debug('Entering: get_issues_user')
    lst = requests.get(URL + '/issues?full=true&username={}&limit=53'.format(user)).json()
    logger.debug(lst)
    if lst['issues']:
        return __to_issue_list(lst)
    else:
        raise NoneFoundError('No issues found for user {}'.format(user))


def get_issues_loc(lat: float, lon: float, rad: int) -> list:
    """
        searches for Issues around a Location

        Attributes
        ----------
        lat : float
            Latitude
        lon : float
            Longitude
        rad : int/float
            search Radius in meters

        Returns
        -------
        list[Issue]
            up to 50 Issues found there.

        Raises
        ------
        NoneFoundError
    """

    logger.debug('Entering: get_issues_loc with (lat:{}, lon:{})'.format(lat, lon))
    bbox = osm_util.create_bbox(lat, lon, rad)
    path = '/issues?full=true&bbox={},{},{},{}&limit=50'
    path = path.format(*bbox)
    lst = requests.get(URL + path).json()
    if lst['issues']:
        return __to_issue_list(lst)
    else:
        raise NoneFoundError('No issues found in {}m around location: {},{}'.format(rad, lat, lon))


def __to_issue_list(issue_lst: dict) -> list:
    """transforms your osmose response list to a list of Issue objects"""
    logger.debug('to issue list')
    lst = []
    for issue in issue_lst['issues']:
        lst.append(__from_api_issue(issue))
    logger.debug('Issue Items: ' + str(len(lst)))
    return lst


def __from_api_issue(lst: dict) -> Issue:
    """transforms your response from osmose api to Issue object"""

    elems = []
    keys = {'nodes': 'node', 'ways': 'way', 'relations': 'rel'}
    for key in lst['osm_ids'].keys():
        i_type = keys[key]
        for i_id in lst['osm_ids'][key]:
            elems.append(osm_util.MicroElem(i_id, i_type))
    issue = Issue(lst['lat'], lst['lon'], lst['id'], lst['title']['auto'], lst['subtitle'], elems)
    return issue


def get_issue(issue_id: str) -> Issue:
    """
        Gives more Information to a specific Issue.

        Attributes
        ----------
        issue_id : str

        Returns
        -------
        Issue
            extended issue
    """

    logger.debug('Entering: get_issue')
    as_json = requests.get(URL + '/issue/{}'.format(issue_id)).json()
    logger.debug(as_json)
    bbox = itemgetter('minlon', 'minlat', 'maxlon', 'maxlat')(as_json)
    elems = []
    for elem in as_json['elems']:
        elems.append(osm_util.MicroElem(elem['id'], elem['type'], elem['tags']))

    issue = Issue(as_json['lat'], as_json['lon'], issue_id,
                  as_json['title'], as_json['subtitle'], elems, bbox)
    return issue


class Pager:
    def __init__(self, lst, step=10):
        self.lst = lst
        self.index = step * (-1)
        self.step = step

    def next(self):
        items = []
        if (len(self.lst) - self.index) < self.step:
            items = self.lst[self.index:]
        else:
            self.index += self.step
            items = self.lst[self.index: (self.index + self.step)]
        logger.debug('pager index after next:' + str(self.index))
        return items

    def prev(self):
        items = []
        if self.index > 0:
            items = self.lst[(self.index - self.step): self.index]
            self.index -= self.step
        else:
            items = self.lst[(self.index - self.step): self.index]
            self.index = 0
        logger.debug('pager index after prev:' + str(self.index))
        return items

    @staticmethod
    def to_msg(lst):
        message = ''
        for item in lst:
            message += str(item) + '\n\n'
        logger.debug(message)
        return message

    def curr(self):
        return self.lst[self.index: (self.index + self.step)]
