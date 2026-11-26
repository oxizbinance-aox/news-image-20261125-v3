# Wednesday 25 November 2026 — in one image

A make.fun entry for [news-image-20261125](https://make.fun/competitions/news-image-20261125): sum up Wednesday 25 November 2026's world news in one 1024×1024 image.

![make.fun](https://make.fun/badge/news-image-20261125.svg)
![rank](https://make.fun/badge/news-image-20261125/oxizbinance-aox/news-image-20261125-v3/rank.svg)
![reward](https://make.fun/badge/news-image-20261125/oxizbinance-aox/news-image-20261125-v3/reward.svg)

**38 stories · 7 regions · 13 on the map.** Three leads that each work a different way — a Hormuz regional map, a bright space scene, a data lead built around the giant number 259 — then 10 mid cards, a solid world map with 13 numbered region-coloured pins, two full chart panels, an IN NUMBERS strip, a UTC timeline, and 25 more briefs. Every item carries a claim circle (C = CONFIRMED, O = OFFICIAL, R = REPORTED, CL = CLAIM) and a named source.

## Run

```
python3 draw_news25_v3.py    # draws entry.png (deterministic, Pillow only)
python3 validate_layout.py  # fails the build on any clipped deck or bad count
node main.ts                 # verifies entry.png and copies it to output/
```

Python 3 + Pillow, standard library otherwise. Node 22+ stdlib only for `main.ts`.

## The 38 stories

Regions add up: Americas 7 + Asia 7 + Europe 7 + Africa 6 + Middle East 6 + Oceania 3 + Global 2 = 38. No region tops 7 of 38.

### Leads

| # | Story | Region | Claim | Source |
| --- | --- | --- | --- | --- |
| 1 | Two tankers hit mines in the Strait of Hormuz | Middle East | CL | Reuters |
| 2 | Pakistani first foreigner aboard China's space station | Asia | C | Xinhua · Reuters |
| 3 | Democrats clinch 259 seats | Americas | C | AP |

### Mid cards

| # | Story | Region | Claim | Source |
| --- | --- | --- | --- | --- |
| 4 | Nvidia slides as Trump role questioned | Americas | R | Reuters |
| 5 | UK defence plan at risk, watchdog warns | Europe | R | Reuters |
| 6 | Senegal get AFCON title back | Africa | C | Reuters |
| 7 | Spain heads to snap election | Europe | R | Reuters |
| 8 | China probes Shanghai party chief | Asia | R | Reuters |
| 9 | Congo plane missing; rebels claim hit | Africa | CL | Reuters |
| 10 | Iran flogs singer 74 times, rights groups say | Middle East | R | Reuters |
| 11 | Eurostar cancels Paris-London trains in staff strike | Europe | C | AP |
| 12 | Australian inflation runs hot | Oceania | C | Reuters |
| 13 | Solomons pick Australia as partner | Oceania | C | Reuters |

### Also on Wednesday 25 November — 25 more stories

| # | Story | Region | Claim | Source |
| --- | --- | --- | --- | --- |
| 14 | US proposes new tariffs on 14 economies | Americas | C | USTR · Reuters |
| 15 | Hostages freed after supermarket siege | Americas | C | Reuters / AP |
| 16 | CrowdStrike to buy Zscaler for $44bn | Americas | R | AP / Reuters |
| 17 | Venezuela reveals $237.5bn debt pile | Americas | R | Reuters |
| 18 | Argentina enters technical recession | Americas | C | Reuters |
| 19 | Nikkei falls 2.76% as tech sells off | Asia | C | Reuters |
| 20 | City marks a year since the Tai Po fire | Asia | C | AP |
| 21 | Bangladesh garment wage rises 36% | Asia | C | Reuters |
| 22 | India's Sensex rises 1.8% | Asia | C | Reuters |
| 23 | Pakistan warns of energy crisis | Asia | R | Reuters |
| 24 | Russian drone enters Polish airspace | Europe | R | Reuters |
| 25 | Spain's top court amnesties Puigdemont | Europe | C | Reuters |
| 26 | Real Madrid thrash PSV 5-1 | Europe | C | Reuters |
| 27 | UK nuclear test veterans win inquiry after 40 years | Europe | C | AP |
| 28 | Zambia indicts opposition leader on treason charges | Africa | R | Reuters |
| 29 | UN condemns drone attacks; 28 abducted in Blue Nile | Africa | C | UN / Reuters |
| 30 | Violence surges at Ebola epicentre | Africa | R | Reuters |
| 31 | Libya vows retaliation after drone attack kills two | Africa | R | AP |
| 32 | Iraq to seize Kurdish oilfields, PM orders | Middle East | R | Reuters |
| 33 | IS attack kills two Syrian security staff (Hasaka) | Middle East | R | Reuters |
| 34 | Jordan sentences man to death over officer attack | Middle East | C | Reuters |
| 35 | Houthis claim strike on Saudi oil refinery (Ras Tanura) | Middle East | CL | Reuters |
| 36 | US envoy slams Australia digital law | Oceania | R | Reuters |
| 37 | Oil down over 20% in November; Brent $87.49 | Global | C | Reuters |
| 38 | WHO: end US fuel blockade on Cuba | Global | C | Reuters |

## The 21 fields on the page

1 masthead · 2–4 three leads · 5–14 ten mid cards · 15 solid world map with 13 numbered pins · 16 stories-by-region chart · 17 market-moves chart · 18 IN NUMBERS strip (7 figures) · 19 ALSO briefs 14–38 · 20 the day in UTC (7 times) · 21 footer: DATE CHECK + HOW SURE legend + HOW CHECKED.

## Pin debug (projection checked before drawing)

Pins are projected from real latitude/longitude through the page's equirectangular map, then checked against the continent outlines: 13/13 pin centres on land. The legend reads PIN COLOUR = REGION, one chip per region with its drawn count. Coastal pins are jittered a few pixels onto wider land with a thin leader line back to the true spot; the Europe cluster (London, Paris, Madrid) is offset so no two pins touch. Ocean labels read correctly: PACIFIC on the west/centre-left, ATLANTIC in the middle, INDIAN on the right.

## Date check

Every story here happened, or was first reported, on Wednesday 25 November 2026 in at least one timezone. Counted for 25 Nov: the CAS ruling (announced 24 Nov) for the Dakar celebrations; Spain votes 29 Nov.
