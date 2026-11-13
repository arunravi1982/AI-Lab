import unittest

from app.knowledge_base import search_articles

from app.ticket_store import get_ticket


class HelpdeskToolTests(unittest.TestCase):

    def test_password_article_exists(self):

        results = search_articles(
            "password reset"
        )

        self.assertTrue(
            len(results) > 0
        )

        self.assertIn(
            "Password Reset",
            results[0]["topic"]
        )


    def test_vpn_article_exists(self):

        results = search_articles(
            "VPN connectivity"
        )

        self.assertTrue(
            len(results) > 0
        )


    def test_existing_ticket(self):

        ticket = get_ticket(
            "TICK-1001"
        )

        self.assertIsNotNone(ticket)

        self.assertEqual(
            ticket["status"],
            "In Progress"
        )


    def test_unknown_ticket(self):

        ticket = get_ticket(
            "TICK-9999"
        )

        self.assertIsNone(ticket)


if __name__ == "__main__":

    unittest.main()