import unittest
import osmose


# noinspection SpellCheckingInspection
class OsmoseTest(unittest.TestCase):
    def test_iss_loc(self):
        issues = osmose.get_issues_loc(49.16949, 9.38447, 500)
        print(issues)

    def test_iss_user_pos(self):
        issues = osmose.get_issues_user('jonycoo')
        print(issues)

    def test_iss_user_neg(self):
        issues = osmose.get_issues_user(None)
        print(issues)



if __name__ == '__main__':
    unittest.main()
