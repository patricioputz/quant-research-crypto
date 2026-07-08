import { strategy, exampleRanking } from "@/data/strategy";
import Reveal from "./Reveal";

export default function StrategySection() {
  const { stats, construction } = strategy;
  const longs = exampleRanking.slice(0, construction.nLong);
  const shorts = exampleRanking.slice(-construction.nShort);

  return (
    <section id="strategy" className="border-b border-line">
      <div className="mx-auto max-w-6xl px-6 py-20 md:py-28">
        <Reveal>
          <p className="eyebrow">01 — The Strategy</p>
        </Reveal>
        <Reveal delay={0.06}>
          <h2 className="mt-4 max-w-xl text-3xl font-medium tracking-tight md:text-4xl">
            Rank, rotate, rebalance.
          </h2>
        </Reveal>

        <div className="mt-12 grid gap-10 md:grid-cols-12">
          <Reveal delay={0.1} className="md:col-span-5">
            <dl className="space-y-6">
              <div>
                <dt className="eyebrow">Universe</dt>
                <dd className="mt-1.5 text-sm text-ink-2">
                  10 liquid cryptocurrencies — BTC, ETH, SOL, BNB, ADA, XRP,
                  AVAX, DOT, LINK, DOGE
                </dd>
              </div>
              <div>
                <dt className="eyebrow">Signal</dt>
                <dd className="mt-1.5 text-sm text-ink-2">
                  {stats.lookbackDays}-day trailing return, ranked
                  cross-sectionally each rebalance
                </dd>
              </div>
              <div>
                <dt className="eyebrow">Construction</dt>
                <dd className="mt-1.5 text-sm text-ink-2">
                  Long top{" "}
                  {Math.round((construction.nLong / strategy.universe.length) * 100)}%,
                  short bottom{" "}
                  {Math.round((construction.nShort / strategy.universe.length) * 100)}%,
                  sized inversely to volatility (not equal-weighted)
                </dd>
              </div>
              <div>
                <dt className="eyebrow">Rebalance</dt>
                <dd className="mt-1.5 text-sm text-ink-2">
                  Every {stats.holdDays} days
                </dd>
              </div>
              <div>
                <dt className="eyebrow">Risk controls</dt>
                <dd className="mt-1.5 text-sm text-ink-2">
                  100% gross exposure cap (no leverage), and a per-position
                  liquidation threshold that forces a close-out if a single
                  name loses more than 50% in a day
                </dd>
              </div>
            </dl>
          </Reveal>

          <Reveal delay={0.16} className="md:col-span-7">
            <div className="border border-line bg-panel/70">
              <p className="border-b border-line px-5 py-4 eyebrow">
                Illustrative rebalance — one snapshot, not a specific date
              </p>
              <div className="grid grid-cols-2 divide-x divide-line">
                <div>
                  <p className="px-5 pt-4 font-mono text-[11px] tracking-[0.14em] text-accent">
                    LONG
                  </p>
                  <ul className="px-5 py-3">
                    {longs.map((r) => (
                      <li
                        key={r.ticker}
                        className="flex items-center justify-between border-b border-line/60 py-2 font-mono text-sm last:border-none"
                      >
                        <span className="text-foreground">{r.ticker}</span>
                        <span className="text-accent">
                          +{r.ret.toFixed(1)}%
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <p className="px-5 pt-4 font-mono text-[11px] tracking-[0.14em] text-ink-3">
                    SHORT
                  </p>
                  <ul className="px-5 py-3">
                    {shorts.map((r) => (
                      <li
                        key={r.ticker}
                        className="flex items-center justify-between border-b border-line/60 py-2 font-mono text-sm last:border-none"
                      >
                        <span className="text-foreground">{r.ticker}</span>
                        <span className="text-ink-2">{r.ret.toFixed(1)}%</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </Reveal>
        </div>
      </div>
    </section>
  );
}
