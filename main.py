#!/usr/bin/env python3
"""main.py — entrypoint for make.fun news-image-20261123 (r3).

Python standard library only. Validates the committed entry.png (PNG magic,
IHDR 1024x1024, per-chunk CRCs, IEND trailer, no trailing bytes, <=1 MiB,
IDAT inflates to the exact expected raw size), copies it byte-for-byte to
$MAKEFUN_OUTPUT_DIR/entry.png, then re-reads and re-validates the copy.
Deterministic: the output bytes are exactly the committed file's bytes.
"""
import hashlib
import os
import struct
import sys
import zlib
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
EXPECT_W, EXPECT_H = 1024, 1024

SRC = Path(__file__).resolve().parent / "entry.png"


class ValidationError(ValueError):
    pass


def _u32(b):
    return struct.unpack(">I", b)[0]


def validate_png(data):
    """Raise ValidationError unless data is a whole, correct 1024x1024 PNG."""
    if len(data) == 0:
        raise ValidationError("empty file")
    if len(data) > MAX_BYTES:
        raise ValidationError("file larger than 1 MiB: %d bytes" % len(data))
    if data[:8] != PNG_MAGIC:
        raise ValidationError("bad PNG magic")
    pos = 8
    seen_ihdr = False
    seen_iend = False
    idat = bytearray()
    color_type = None
    bit_depth = None
    while pos < len(data):
        if pos + 8 > len(data):
            raise ValidationError("truncated chunk header at offset %d" % pos)
        length = _u32(data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + length > len(data):
            raise ValidationError("truncated chunk %r at offset %d"
                                  % (ctype, pos))
        payload = data[pos + 8:pos + 8 + length]
        crc_stored = _u32(data[pos + 8 + length:pos + 12 + length])
        crc_actual = zlib.crc32(ctype + payload) & 0xFFFFFFFF
        if crc_actual != crc_stored:
            raise ValidationError("bad CRC in chunk %r at offset %d"
                                  % (ctype, pos))
        if ctype == b"IHDR":
            if seen_ihdr:
                raise ValidationError("duplicate IHDR")
            if pos != 8:
                raise ValidationError("IHDR is not the first chunk")
            if length != 13:
                raise ValidationError("IHDR length is %d, expected 13"
                                      % length)
            w, h = _u32(payload[0:4]), _u32(payload[4:8])
            bit_depth, color_type = payload[8], payload[9]
            if (w, h) != (EXPECT_W, EXPECT_H):
                raise ValidationError("IHDR size %dx%d, expected 1024x1024"
                                      % (w, h))
            if bit_depth != 8:
                raise ValidationError("bit depth %d, expected 8" % bit_depth)
            if color_type not in (2, 6):
                raise ValidationError("color type %d, expected 2 or 6"
                                      % color_type)
            seen_ihdr = True
        elif ctype == b"IDAT":
            if not seen_ihdr:
                raise ValidationError("IDAT before IHDR")
            idat.extend(payload)
        elif ctype == b"IEND":
            if length != 0:
                raise ValidationError("IEND length is %d, expected 0"
                                      % length)
            if pos + 12 != len(data):
                raise ValidationError("trailing bytes after IEND")
            seen_iend = True
            pos += 12
            break
        elif ctype == b"PLTE" and color_type in (2, 6):
            raise ValidationError("PLTE chunk in a truecolour image")
        pos += 12 + length
    if not seen_ihdr:
        raise ValidationError("missing IHDR")
    if not seen_iend:
        raise ValidationError("missing IEND trailer")
    if not idat:
        raise ValidationError("missing IDAT")
    channels = 3 if color_type == 2 else 4
    expected_raw = EXPECT_H * (1 + EXPECT_W * channels)
    try:
        raw = zlib.decompress(bytes(idat))
    except zlib.error as exc:
        raise ValidationError("IDAT does not inflate: %s" % exc)
    if len(raw) != expected_raw:
        raise ValidationError("IDAT inflates to %d bytes, expected %d"
                              % (len(raw), expected_raw))
    return True


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 2
    try:
        data = SRC.read_bytes()
    except OSError as exc:
        print("cannot read %s: %s" % (SRC, exc), file=sys.stderr)
        return 1
    try:
        validate_png(data)
    except ValidationError as exc:
        print("entry.png invalid: %s" % exc, file=sys.stderr)
        return 1
    out_path = Path(out_dir) / "entry.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(data)
    try:
        validate_png(out_path.read_bytes())
    except ValidationError as exc:
        print("output copy invalid: %s" % exc, file=sys.stderr)
        return 1
    print("entry.png OK: %d bytes sha256=%s"
          % (len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
