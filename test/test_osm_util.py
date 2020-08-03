import unittest
import osm.osm_util

class MyTestCase(unittest.TestCase):
    def test_node_to_string(self):
        tags = {'alphabeth': 'acbde', 'numbers': '12345'}
        node = osm.osm_util.Node(None, None, None, None, None, None, None, None, None, tags)
        assert str(node) == 'type: node\n ---- \nalphabeth: acbde\nnumbers: 12345\nloc: None, None'

        node = osm.osm_util.Node(123, 5.2,8.7,5,1234,'testuser',0,'00.00.0000',True, tags)
        assert str(node) == 'node 123\ncreated: 00.00.0000\nversion: 5\nvisible: True\nchangeset: 1234\ntestuser 0\n' \
                            ' ---- \nalphabeth: acbde\nnumbers: 12345\nloc: 5.2, 8.7'




if __name__ == '__main__':
    unittest.main()
