#!/usr/bin/env python3
"""test_negative.py — negative tests for main.py's PNG validator.

Mutates the committed entry.png in memory only (never writes to disk) and
checks every mutation is rejected. Run: python3 test_negative.py
Exit 0 when all mutations are rejected and the valid file passes.
"""
import struct
import sys
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from main import validate_png, ValidationError, SRC  # noqa: E402


def _fix_ihdr_crc(data):
    """Recompute the IHDR chunk CRC after an in-place IHDR edit."""
    data = bytearray(data)
    crc = zlib.crc32(bytes(data[12:12 + 4 + 13])) & 0xFFFFFFFF
    # IHDR chunk: length@8, type@12, data@16..28, CRC@29..32
    data[29:33] = struct.pack(">I", crc)
    return bytes(data)


def _find_chunk(data, want):
    pos = 8
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        if ctype == want:
            return pos, length
        pos += 12 + length
    raise AssertionError("chunk %r not found" % want)


def main():
    good = SRC.read_bytes()
    cases = {}

    # 1. bad magic
    bad = bytearray(good)
    bad[0] = 0x00
    cases["bad magic"] = bytes(bad)

    # 2. wrong width (CRC fixed so only the size check can catch it)
    bad = bytearray(good)
    bad[16:20] = struct.pack(">I", 512)
    cases["wrong width 512 (CRC fixed)"] = _fix_ihdr_crc(bytes(bad))

    # 3. wrong height (CRC fixed)
    bad = bytearray(good)
    bad[20:24] = struct.pack(">I", 512)
    cases["wrong height 512 (CRC fixed)"] = _fix_ihdr_crc(bytes(bad))

    # 4. bad CRC (flip a byte inside the IHDR CRC field @29..32)
    bad = bytearray(good)
    bad[29] ^= 0xFF
    cases["bad IHDR CRC"] = bytes(bad)

    # 5. truncated (drop the last 20 bytes, cutting into IEND)
    cases["truncated"] = good[:-20]

    # 6. trailing bytes after IEND
    cases["trailing bytes"] = good + b"junkjunk"

    # 7. empty file
    cases["empty"] = b""

    # 8. corrupt IDAT (flip the first byte of the first IDAT payload:
    #    breaks the zlib stream header)
    pos, _length = _find_chunk(good, b"IDAT")
    bad = bytearray(good)
    bad[pos + 8] ^= 0xFF
    cases["corrupt IDAT"] = bytes(bad)

    # 9. missing IEND (drop the final 12-byte chunk)
    cases["missing IEND"] = good[:-12]

    failures = []
    try:
        validate_png(good)
        print("PASS: valid file accepted")
    except ValidationError as exc:
        failures.append("valid file rejected: %s" % exc)
        print("FAIL: valid file rejected: %s" % exc)

    for name, data in cases.items():
        try:
            validate_png(data)
            failures.append(name)
            print("FAIL: %-32s accepted (should be rejected)" % name)
        except ValidationError as exc:
            print("PASS: %-32s rejected (%s)" % (name, exc))

    if failures:
        print("%d failure(s)" % len(failures))
        return 1
    print("all %d negative cases rejected, valid file accepted" % len(cases))
    return 0


if __name__ == "__main__":
    sys.exit(main())
