import unittest
import database
from sqlite3 import Error, IntegrityError


class MyTestCase(unittest.TestCase):

    def prep(self):
        db = database.DBLite()
        db.create_connection('userdata.db')
        return db

    def test_insert(self):
        db = self.prep()
        db.insert_credentials(0, 'abc', 'def')
        db.insert_credentials(1, None, None)
        self.assertEqual(db.select_credentials(0), ('abc', 'def'))
        self.assertEqual(db.select_credentials(1), (None, None))

    def test_update(self):
        db = self.prep()
        db.insert_credentials(0, None, None)
        db.update_credentials(0, 'anja', 'mueller')
        self.assertEqual(db.select_credentials(0), ('anja', 'mueller'))

    def test_fail_update(self):
        db = self.prep()
        with self.assertRaises(IntegrityError):
            db.update_credentials(12, 'abc', 'def')
        db.connection.close()

    def test_delete(self):
        db = self.prep()
        db.insert_credentials(12, 'anna', 'maquat')
        db.delete_credentials(12)
        self.assertEqual(db.select_credentials(12), None)

    def test(self):
        pass



if __name__ == '__main__':
    unittest.main()
