import unittest
import arrow
import flask_main

class TestMemoDB(unittest.TestCase):

    def testHumanizingDate(self):
        #Testing today case
        test_date = arrow.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        self.assertEqual(flask_main.humanize_arrow_date(test_date), "Today")

        #Testing yesterday case
        self.assertEqual(flask_main.humanize_arrow_date(test_date.replace(days=-1)), "Yesterday")

        #Testing 2 days ago case
        self.assertEqual(flask_main.humanize_arrow_date(test_date.replace(days=-2)), "2 days ago")

        #Testing tomorrow case
        test_date = test_date.replace(days=+1)
        self.assertEqual(flask_main.humanize_arrow_date(test_date), "Tomorrow")

        #Testing other day cases up to where arrow defines it as a month
        for h in range(2, 24):
            test_date = test_date.replace(days=+1)
            self.assertEqual(flask_main.humanize_arrow_date(test_date), "in {} days".format(h))

    def testSavingMemo(self):
        date = '2016-02-11'
        text = "Sample text"
        result = flask_main.new_memo(date, text)
        #print(result)
        #print("\n")

    def testListingMemos(self):
        listed_memos = flask_main.get_memos()
        #print(listed_memos)
        #print("\n")

    def testDeletingMemos(self):
        removeIds = []
        for record in flask_main.collection.find({"text":"Sample text"}):
            removeIds.append(str(record['_id']))

        deleted = flask_main.remove_memos(removeIds)
        #print(deleted)


if __name__ == '__main__':
    unittest.main()
