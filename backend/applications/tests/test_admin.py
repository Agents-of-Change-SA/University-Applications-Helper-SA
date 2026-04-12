from django.test import TestCase

from applications.admin import ApplicationEntryAdmin


class ApplicationEntryAdminTest(TestCase):
    def test_list_display(self):
        self.assertEqual(
            ApplicationEntryAdmin.list_display,
            ('institution_name', 'open_date', 'close_date',
             'application_fee', 'portal_url'),
        )

    def test_list_filter(self):
        self.assertEqual(
            ApplicationEntryAdmin.list_filter,
            ('open_date', 'close_date'),
        )

    def test_search_fields(self):
        self.assertEqual(
            ApplicationEntryAdmin.search_fields,
            ('institution_name',),
        )
