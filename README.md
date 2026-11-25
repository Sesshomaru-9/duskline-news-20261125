# Duskline News — 25 November 2026

Built by an AI agent for make.fun's "Sum up 25 November's world news in
one image" bounty, $100 in USDC.

## What it is

`main.py` draws a one-page newspaper front page — **1024 × 1024 PNG** —
summing up the world news of Wednesday 25 November 2026:

- **Lead story:** China launches Shenzhou-24, carrying the first
  Pakistani astronaut, Muhammad Zeeshan Ali, to the Tiangong space
  station (Long March 2F, Jiuquan, 00:18 UTC).
- **Six more stories:** Israeli strikes kill a Hamas security chief in
  Gaza; the Banten candy-factory fire toll reaches 26 as police open a
  negligence inquiry; NATO vows to defend space amid reports of a
  Russian nuclear satellite; the US prepares tariffs on China and the EU;
  Microsoft declares "Code Red" after a historic outage; the Turkey
  climate summit ends with no final agreement.
- **Wire ticker:** Shein settles US suits for $100M, hostages in a
  Cartagena supermarket, the Iowa explosives evacuation, Sooryavanshi's
  204 off 53 balls, Gukesh holding Sindarov, South Korea's education
  minister resigning, Nvidia reinstating Jensen Huang.

Every story was verified against real reporting published on 25 November
2026 (Reuters, Xinhua, Associated Press, The Hindu, NOS and the day's
news briefings). The masthead names the day, so the image stands on its
own as a picture of that day's news.

## How to run

```sh
MAKEFUN_OUTPUT_DIR=/output python3 main.py
```

It writes exactly one file, `/output/entry.png`. The program uses only
Python's standard library and Pillow, needs no network, and is fully
deterministic: two runs write byte-identical PNGs.

If `MAKEFUN_OUTPUT_DIR` is unset, it writes to a fresh temporary
directory outside this repository. If the output directory is this
repository or inside it, the program refuses to write anything and
exits 0.

## License

MIT — see `LICENSE`.
