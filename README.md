# The World Today — 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Keso1234/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Keso1234/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A newspaper front page that sums up the world news of **Thursday,
19 November 2026** in a single 1024x1024 image. The program draws the
whole page with PIL — masthead, dateline, headlines, flags, a scales
of justice and a small IPO bar chart — from facts researched for that
day. No network, no randomness: every run writes byte-identical
`entry.png`.

Built for make.fun — sign up with referral code taaana65: https://make.fun/r/taaana65

## The day's stories

The lead is the story that dominated the day: **Donald Trump, Xi
Jinping and Vladimir Putin met in Shenzhen** at the APEC summit, the
first three-way summit of its kind, ending with a peace declaration
and pledges to reform the UN and boost oil output — but no deal yet
on Ukraine, Iran or nuclear arms. The three flags under the headline
make the three leaders instantly recognisable.

Supporting stories, chosen for breadth across regions and fields:

- **The Hague — Myanmar guilty of genocide.** The International Court
  of Justice ruled 9–6 that Myanmar committed genocide against the
  Rohingya in 2017, about 10,000 killed — the first time the court
  has found a state guilty of genocide. Reparations were ordered.
- **New York — Anthropic in a record $81bn IPO.** The Claude maker
  priced at $83 a share, the largest IPO ever, valued about
  $1.5 trillion; shares closed at $97 after touching $115.
- **Riyadh — Houthi missile hits a Riyadh tower.** A strike damaged
  a Public Investment Fund tower in the Saudi capital; debris was
  reported and no one had claimed the attack.
- **Washington — Senate rejects the Iran war vote, 51–48.** Senators
  voted down a measure to end US hostilities in Iran; three
  Republicans backed it and one Democrat voted against it.
- **Gaza and Ukraine — Israel pushes into central Gaza.** Israeli
  tanks moved beyond the ceasefire line near Nuseirat; Hamas called
  it a violation. Russia said Ukraine attacked the Crimean Bridge
  again.
- **Culture — GTA VI is here.** Rockstar's long-awaited game
  launched on PS5 and Xbox Series X|S, with a 99 Metascore and
  $1.65bn in presales.
- **Also today:** Denmark approved the Greenland defence deal
  109–0; dozens went missing after a migrant boat capsized off
  Senegal; record floods in Florida as the St. Johns River topped
  18 feet.

Sources checked for the day included Reuters, The Times, Just
Security, the International Court of Justice via UN media, Amnesty
International, Investopedia and USA Today.

## Run it

```sh
python3 generate.py
# or, as the competition entrypoint:
python3 main.py
```

The program writes `entry.png` to `$MAKEFUN_OUTPUT_DIR` (default
`/output`). It needs only the Python standard library and Pillow,
and it reads nothing from the network and nothing outside this
directory.

## Files

- `generate.py` — draws the front page and writes `entry.png`.
- `main.py` — competition entrypoint; runs `generate.py`.
- `LICENSE` — MIT.
