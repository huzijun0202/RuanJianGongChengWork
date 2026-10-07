"""HJ212-2017 protocol message parser.

The parser focuses on the wire format used by HJ212-2017:
``##`` + four-digit data length + data segment + four-digit CRC + CRLF.
"""

from __future__ import annotations

import re
from typing import Dict


class HJ212Parser:
    """Validate and parse HJ212-2017 messages."""

    HEADER = b"##"
    TRAILER = b"\r\n"
    _LENGTH_RE = re.compile(rb"^##(?P<length>\d{4})")

    @staticmethod
    def _as_bytes(message: str | bytes) -> bytes:
        if isinstance(message, bytes):
            return message
        if isinstance(message, str):
            return message.encode("ascii")
        raise TypeError("message must be str or bytes")

    def _parts(self, message: str | bytes) -> tuple[bytes, bytes, bytes] | None:
        raw = self._as_bytes(message)
        match = self._LENGTH_RE.match(raw)
        if not match or not raw.endswith(self.TRAILER):
            return None
        data_length = int(match.group("length"))
        data_start = match.end()
        data_end = data_start + data_length
        crc_end = data_end + 4
        if crc_end + len(self.TRAILER) != len(raw):
            return None
        data = raw[data_start:data_end]
        crc = raw[data_end:crc_end]
        if not re.fullmatch(rb"[0-9A-Fa-f]{4}", crc):
            return None
        return raw, data, crc

    def is_valid_message(self, message: str | bytes) -> bool:
        """Return whether framing, length, CRC and terminator are valid."""
        try:
            parts = self._parts(message)
        except (UnicodeEncodeError, TypeError):
            return False
        return parts is not None and self.validate_crc(message)

    @staticmethod
    def _crc16_ansi(data: bytes) -> int:
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
        return crc & 0xFFFF

    def validate_crc(self, message: str | bytes) -> bool:
        """Validate the four hexadecimal CRC characters in a message."""
        try:
            parts = self._parts(message)
        except (UnicodeEncodeError, TypeError):
            return False
        if parts is None:
            return False
        _, data, supplied = parts
        expected = f"{self._crc16_ansi(data):04X}".encode("ascii")
        return supplied.upper() == expected

    def parse_data_segment(self, message: str | bytes) -> Dict[str, str]:
        """Parse the data segment into key/value pairs.

        HJ212 commonly separates fields with semicolons. Bare fields are
        retained with an empty value so no information is silently discarded.
        """
        parts = self._parts(message)
        if parts is None:
            raise ValueError("invalid HJ212 message framing")
        _, data, _ = parts
        try:
            text = data.decode("ascii")
        except UnicodeDecodeError as exc:
            raise ValueError("data segment is not ASCII") from exc
        parsed: Dict[str, str] = {}
        for field in text.split(";"):
            if not field:
                continue
            key, separator, value = field.partition("=")
            if not key:
                raise ValueError("data segment contains an empty key")
            parsed[key] = value if separator else ""
        return parsed

    def extract_monitoring_data(self, message: str | bytes) -> Dict[str, str]:
        """Extract monitoring-factor values from CP fields.

        CP fields may be represented as ``CP=&&k=v&k2=v2&&`` or directly as
        ``CP=&&DataTime=...&w01001-Rtd=...&&``. Keys are returned without the
        CP wrapper; non-CP fields remain available through ``parse_data_segment``.
        """
        fields = self.parse_data_segment(message)
        monitoring: Dict[str, str] = {}
        for key, value in fields.items():
            if key.upper() != "CP":
                continue
            inner = value.strip("&")
            for item in inner.split("&"):
                if not item:
                    continue
                factor, separator, factor_value = item.partition("=")
                if factor and separator:
                    monitoring[factor] = factor_value
        return monitoring


__all__ = ["HJ212Parser"]
