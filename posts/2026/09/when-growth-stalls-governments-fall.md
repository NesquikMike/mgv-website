---
title: When Growth Stalls, Governments Fall
date: 2026-09-11
layout: blog-post.11ty.js
---

Andy Burnham became Britain's seventh prime minister in a decade on 20 July. Keir Starmer had lasted barely two years. Before him came Sunak, Truss, Johnson, and May. France has cycled through Barnier and Bayrou under Macron. Germany elected Friedrich Merz in May.

The turnover feels exceptional. I wanted to know whether it is, and whether it tracks something simpler than ideology: GDP growth.

## What I measured

I pulled leader and coalition change dates for 20 Western democracies from [ParlGov](http://www.parlgov.org/){target="_blank" rel="noopener"}, with manual overrides for events after the dataset ends (including Burnham's appointment). For each country I count an **either-change** in any rolling window where the prime minister, president, or governing coalition changed. The Western average is the mean across countries.

GDP comes from the World Bank: cross-country mean year-on-year growth in GDP per capita, smoothed over five years.

<figure class="captioned-image">
  <img src="/assets/images/posts/western-political-instability/either-change-rate.png" alt="Either-change rate for 20 Western democracies from 1950 to 2026, with 5-year and 10-year rolling windows"></img>
  <figcaption>Either-change rate across 20 Western democracies, 1950–2026</figcaption>
</figure>

The headline is not that turnover is at an all-time high. The 1980s were worse. What stands out is the shape since 2000: a trough in the 2000s (about 0.27 changes per country per year), then a climb through the 2010s (about 0.35). Brexit, Trump, Macron's hung parliament, Italy's revolving door, and the post-COVID inflation fights all sit on that upswing.

## Growth and turnover

Overlaying GDP growth on the same series shows a long downward drift in growth alongside the post-2000s rise in turnover.

<figure class="captioned-image">
  <img src="/assets/images/posts/western-political-instability/instability-vs-gdp-growth.png" alt="Either-change rate and 5-year GDP growth for Western democracies, 1960 to 2025"></img>
  <figcaption>Political turnover and GDP growth, 1960–2025</figcaption>
</figure>

Raw growth is noisy. A recession year does not always coincide with a leadership change. So I tried a cruder stress measure: how far the five-year growth rate has fallen below its own ten-year trailing average. Zero means growth is at or above trend; higher means a sustained shortfall.

<figure class="captioned-image">
  <img src="/assets/images/posts/western-political-instability/instability-vs-gdp-stress.png" alt="Either-change rate against lagged GDP growth stress for Western democracies"></img>
  <figcaption>GDP growth stress (one-year lead) against political turnover</figcaption>
</figure>

The peaks line up often enough to notice: the mid-1970s oil shocks, the early 1980s, 2008–09, COVID. Pearson correlation between stress and turnover is r = 0.31 at zero lag and r = 0.27 at one year. That is weak. You would not trade on it. But it is stronger than I expected from 60 annual data points averaged across heterogeneous countries.

## What this does not prove

Correlation is not causation. Japan and Italy have high leader turnover even in decades of modest growth. Luxembourg tops the league table since 2000 on a tiny base. The UK sample is seven prime ministers in a decade partly because of party-internal coups, not elections lost to recession.

The aggregate also hides timing. A growth shock in Germany in 2009 does not force a Belgian coalition collapse in the same quarter. Lagging stress by one year is a visual choice as much as a statistical one: it lets a growth drop appear before the political response on the chart.

Still, the pattern fits a simple story. When living standards stop improving on the timetable voters have come to expect, governments that promised competence start looking disposable. Britain's revolving door is an extreme case. The Western average suggests something broader shifted after the 2000s calm.

I have almost certainly missed an override or two; corrections welcome.
