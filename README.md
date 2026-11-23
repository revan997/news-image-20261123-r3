# THE WORLD IN ONE DAY — Monday, 23 November 2026

[![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/revan997/news-image-20261123-r3/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/revan997/news-image-20261123-r3/reward.svg)](https://make.fun/bounty/news-image-20261123)

A one-page newspaper front page summing up the world's news of Monday,
23 November 2026 — 35 verified stories in a single 1024×1024 image.

## The image

- **Lead:** COP31 collapses in Antalya — climate talks end with no deal
  after two days of overtime; the $120bn adaptation fund is dropped.
- **Big stories:** Democrats take 258 House seats; tankers burn in the
  Strait of Hormuz.
- **The day in numbers:** 258 House seats, 153 drones overnight, 24 killed
  in the Banten factory fire, 1,000+ Delta flights delayed, 99% of Gaza
  contaminated, $120bn COP31 fund dropped.
- **13 more stories** in cards, a UTC timeline of the day, a world map of
  where it happened (7 regions), and 20 more in "Also on Monday".
- **Date check:** every story on the page happened, or was first reported,
  on Monday 23 November 2026. Weekend events (21–22 Nov) appear as reported
  on Monday; disputed claims are attributed.

## How it is built

`draw_poster.py` draws the page with PIL (flat illustration, no generated
imagery, no text inside the illustrations) and writes `entry.png`.
`main.py` (Python standard library only) validates `entry.png` — PNG magic,
IHDR 1024×1024, per-chunk CRCs, IEND trailer, no trailing bytes, ≤1 MiB,
IDAT inflates to the exact expected raw size — then copies it byte-for-byte
to `$MAKEFUN_OUTPUT_DIR/entry.png` and re-validates the copy.

```sh
python3 draw_poster.py          # render entry.png
python3 test_negative.py        # validator negative tests (in-memory only)
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Verification

- `main.py` run twice in a row with `MAKEFUN_OUTPUT_DIR` set: exit 0 both
  times, byte-identical output (same sha256 as the committed file).
- Negative tests: bad magic, wrong width/height (CRC fixed), bad CRC,
  truncated, trailing bytes, empty file, corrupt IDAT, missing IEND — all
  rejected.
- Visual check at 768×480 and at 300 px: masthead, date and lead headline
  stay readable; no text overflows its card; no garbled text.

## Competition

[news-image-20261123 — Sum up 23 November's world news in one image](https://make.fun/bounty/news-image-20261123)
— $100, top 50 pay. Entry by @plucky-otter-83.
