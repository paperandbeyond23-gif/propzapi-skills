"""Smoke tests for the propzapi-props handler. No network — urlopen is mocked."""

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
            result = handler.get_props(league="NBA")
        self.assertEqual(result["error"], "auth_required")
        self.assertEqual(result["signup_url"], "https://propzapi.com/app")


class TestEndpoints(unittest.TestCase):
    @patch("handler.urllib.request.urlopen")
    def test_props_hits_v1_props(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"count": 0, "data": []}')
        with patch.dict(os.environ, {"PROPZAPI_KEY": "pk_live_test"}):
            handler.get_props(league="NBA", limit=5)
        req = _req(mock_urlopen)
        self.assertIn("/v1/props", req.full_url)
        self.assertEqual(req.headers["X-api-key"], "pk_live_test")

    @patch("handler.urllib.request.urlopen")
    def test_events_hits_v1_events(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"count": 0, "data": []}')
        with patch.dict(os.environ, {"PROPZAPI_KEY": "pk_live_test"}):
            handler.get_events(league="EPL", status="live")
        self.assertIn("/v1/events", _req(mock_urlopen).full_url)

    def test_events_rejects_bad_status(self):
        with patch.dict(os.environ, {"PROPZAPI_KEY": "pk_live_test"}):
            self.assertEqual(handler.get_events(status="over")["error"], "invalid_argument")


class TestErrorMapping(unittest.TestCase):
    @patch("handler.urllib.request.urlopen")
    def test_402_out_of_credits(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError("u", 402, "e", {}, None)
        with patch.dict(os.environ, {"PROPZAPI_KEY": "pk_live_test"}):
            out = handler.get_props(league="NBA")
        self.assertEqual(out["error"], "out_of_credits")


if __name__ == "__main__":
    unittest.main()
