import unittest
import ee_osmose
import osm.osm_api as osmapi
import osm.osm_util


class MyTestCase(unittest.TestCase):
    osmo = osmapi.OsmApi()

    def test_permissions(self):
        data = self.osmo.get_permissions()
        print(data)

    def test_cs_cre(self):
        data = self.osmo.create_changeset({'comment': 'test', 'created_by': 'osmate'})
        print(data)

    def test_cs_sub(self):
        data = self.osmo.sub_changeset(177967)
        print(data)

    def test_cs_unsub(self):
        data = self.osmo.unsub_changeset(177967)
        print(data)

    def test_cs_get(self):
        cs = self.osmo.get_changeset(177967)
        print(cs)

    def test_cs_comment(self):
        cs = self.osmo.comm_changeset(177967, 'Hallo Welt')
        print(cs)

    def test_get_node(self):
        node = self.osmo.get_element('node', 4314858041)
        print(node.__repr__())

    def test_get_way(self):
        node = self.osmo.get_element('way', 201774)
        print(node.__repr__())

    def test_get_relation(self):
        rel = self.osmo.get_element('relation', 4304875773)
        print(rel.__repr__())

    def test_get_mutiple_elem(self):
        rel = self.osmo.get_elements('way', [201774, 4305504687])
        for item in rel:
            print(item.__repr__)

    def test_get_elem_bbox_pos(self):
        # westlimit=9.3852744541; southlimit=49.1700528219; eastlimit=9.38678722; northlimit=49.1708595043
        print(osm.osm_util.create_bbox(52.5134, 13.4374, 1000))
        elems = self.osmo.get_element_bbox((13.428416654163087, 52.49863874116848, 13.446383345836914, 52.52816125883152))
        for item in elems:
            print(item.__repr__)

    def test_get_elem_bbox_neg(self):
        with self.assertRaises(ee_osmose.NoneFoundError):
            # westlimit=9.3852744541; southlimit=49.1700528219; eastlimit=9.38678722; northlimit=49.1708595043
            print(osm.osm_util.create_bbox(52.5134, 13.4374, 1000))
            elems = self.osmo.get_element_bbox((9.3849565809, 49.1700030402, 9.3867590254, 49.1707360702))
            for item in elems:
                print(item.__repr__)

    def test_get_gpx_bbox(self):
        # 46.7723/12.1855
        print(osm.osm_util.create_bbox(46.7723, 12.1855, 500))
        gpx = self.osmo.get_bbox_gpx(osm.osm_util.create_bbox(46.7723, 12.1855, 750), 0)

    def test_send_gpx(self):
        gpx = open('/home/marvin/Downloads/2020-05-31_15-23_Sun.gpx').read()
        tid = self.osmo.upload_gpx(gpx, 'test_trace.xml', 'test', {'test', 'osmate'})
        print(tid)

#   only works with defined value
#    def test_delete_gpx(self):
#        self.osmo.delete_gpx()

    def test_get_own_gpx(self):
        list_gpx = self.osmo.get_own_gpx()
        print(list_gpx)

    def test_get_notes_bbox(self):
        notes = self.osmo.get_notes_bbox((13.428416654163087, 52.49863874116848, 13.446383345836914, 52.52816125883152))
        print(notes[0])

    def tests_get_note(self):
        note = self.osmo.get_note(22599)
        print(note)

    def test_close_note(self):
        data = self.osmo.close_note(22599, 'abc')
        print(data)

    def test_edit_elem(self):
        node = self.osmo.get_element('node', 4314858041)
        data = self.osmo.edit_element(node, 178488)
        print(data)

    def test_get_users(self):
        users = self.osmo.get_users([7634, 7122])
        print(users)


if __name__ == '__main__':
    unittest.main()
