"""Smoke tests for the propzapi-odds handler. No network — urlopen is mocked."""

import os
import sys
import unittest
import urllib.error
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import handler  # noqa: E402


def _mock_response(body):
    cm = MagicMock()
    cm.__enter__.return_value.read.return_value = body
    return cm


def _req(mock_urlopen):
    return mock_urlopen.call_args[0][0]


class TestAuth(unittest.TestCase):
    def test_missing_key_returns_auth_required(self):
        with patch.dict(os.environ, {}, clear=True):
            result = handler.get_odds(league="NBA")
        self.assertEqual(result["error"], "auth_required")
        self.assertEqual(result["signup_url"], "https://propzapi.com/app")


class TestEndpoints(unittest.TestCase):
    @patch("handler.urllib.request.urlopen")
    def test_odds_hits_v1_odds(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"count": 0, "data": []}')
        with patch.dict(os.environ, {"PROPZAPI_KEY": "pk_live_test"}):
            handler.get_odds(league="NBA", market="spreads")
        req = _req(mock_urlopen)
        self.assertIn("/v1/odds", req.full_url)
        self.assertIn("market=spreads", req.full_url)
        self.assertEqual(req.headers["X-api-key"], "pk_live_test")

    @patch("handler.urllib.request.urlopen")
    def test_books_hits_v1_books(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"books": [], "count": 0}')
        with patch.dict(os.environ, {"PROPZAPI_KEY": "pk_live_test"}):
            handler.get_books()
        self.assertTrue(_req(mock_urlopen).full_url.endswith("/v1/books"))

    def test_odds_rejects_bad_market(self):
        with patch.dict(os.environ, {"PROPZAPI_KEY": "pk_live_test"}):
            self.assertEqual(handler.get_odds(market="parlay")["error"], "invalid_argument")


class TestErrorMapping(unittest.TestCase):
    @patch("handler.urllib.request.urlopen")
    def test_401_auth_invalid(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError("u", 401, "e", {}, None)
        with patch.dict(os.environ, {"PROPZAPI_KEY": "pk_live_test"}):
            self.assertEqual(handler.get_odds(league="NBA")["error"], "auth_invalid")


if __name__ == "__main__":
    unittest.main()
