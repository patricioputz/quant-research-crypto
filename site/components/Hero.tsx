import type { CurvePoint } from "@/lib/data";
import { strategy } from "@/data/strategy";
import Reveal from "./Reveal";
import CountUp from "./CountUp";

function Sparkline({ points }: { points: CurvePoint[] }) {
  const w = 148;
  const h = 34;
  const pad = 4;
  const step = Math.max(1, Math.floor(points.length / 72));
  const sampled = points.filter(
    (_, i) => i % step === 0 || i === points.length - 1
  );
  const vals = sampled.map((p) => Math.log(p.strategy));
  const min = Math.min(...vals);
  const max = Math.max(...vals);
  const x = (i: number) => pad + (i / (vals.length - 1)) * (w - pad * 2);
  const y = (v: number) => h - pad - ((v - min) / (max - min)) * (h - pad * 2);
  const d = vals
    .map((v, i) => `${i === 0 ? "M" : "L"}${x(i).toFixed(1)},${y(v).toFixed(1)}`)
    .join("");
  return (
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} aria-hidden="true">
      <path d={d} fill="none" stroke="var(--accent)" strokeWidth="1.5" />
      <circle
        cx={x(vals.length - 1)}
        cy={y(vals[vals.length - 1])}
        r="2.5"
        fill="var(--accent)"
        stroke="var(--background)"
        strokeWidth="1.5"
      />
    </svg>
  );
}

export default function Hero({ curve }: { curve: CurvePoint[] }) {
  const { stats, construction, universe } = strategy;
  const sharpe = Math.round(stats.sharpe * 100) / 100;
  const maxDdPct = Math.round(Math.abs(stats.maxDrawdown) * 100);

  return (
    <section id="top" className="relative overflow-hidden border-b border-line">
      <div className="hero-grid pointer-events-none absolute inset-0" aria-hidden="true" />
      <div className="relative mx-auto grid max-w-6xl gap-14 px-6 pb-20 pt-20 md:grid-cols-12 md:pb-28 md:pt-28">
        <div className="md:col-span-7">
          <Reveal>
            <p className="eyebrow">{strategy.eyebrow} — 001</p>
          </Reveal>
          <Reveal delay={0.06}>
            <h1 className="mt-5 max-w-xl text-[2.6rem]/[1.06] font-medium tracking-tight md:text-6xl/[1.04]">
              Cross-Sectional Momentum
            </h1>
          </Reveal>
          <Reveal delay={0.12}>
            <p className="mt-6 max-w-md text-base/relaxed text-ink-2">
              {strategy.oneLiner}
              <span className="cursor-blink" aria-hidden="true" />
            </p>
          </Reveal>
          <Reveal delay={0.18}>
            <p className="mt-10 font-mono text-[11px] tracking-[0.16em] text-ink-3">
              UNIVERSE {universe.length} · LONG {construction.nLong} / SHORT{" "}
              {construction.nShort} · LOOKBACK {stats.lookbackDays}D ·
              REBALANCE {stats.holdDays}D
            </p>
          </Reveal>
        </div>

        <Reveal delay={0.15} className="md:col-span-5">
          <div className="border border-line bg-panel/70">
            <div className="flex items-end justify-between gap-4 border-b border-line px-5 py-4">
              <p className="eyebrow">
                Backtest {strategy.period.start} → {strategy.period.end}
              </p>
              <Sparkline points={curve} />
            </div>
            <dl className="divide-y divide-line">
              <div className="flex items-baseline justify-between px-5 py-5">
                <div>
                  <dt className="eyebrow">Sharpe — full history</dt>
                  <p className="mt-1.5 font-mono text-[10px] tracking-[0.14em] text-ink-3">
                    FIXED CONFIG · √365
                  </p>
                </div>
                <dd className="font-mono text-4xl tabular-nums text-foreground">
                  <CountUp value={sharpe} decimals={2} />
                </dd>
              </div>
              <div
                className="flex items-baseline justify-between px-5 py-5"
                style={{ boxShadow: "inset 2px 0 0 var(--accent)" }}
              >
                <div>
                  <dt className="eyebrow">Sharpe — out-of-sample</dt>
                  <p className="mt-1.5 font-mono text-[10px] tracking-[0.14em] text-ink-3">
                    7-WINDOW WALK-FORWARD
                  </p>
                </div>
                <dd className="font-mono text-4xl tabular-nums text-foreground">
                  <CountUp value={stats.oosSharpeAvg} decimals={2} />
                </dd>
              </div>
              <div className="flex items-baseline justify-between px-5 py-5">
                <div>
                  <dt className="eyebrow">Max drawdown</dt>
                  <p className="mt-1.5 font-mono text-[10px] tracking-[0.14em] text-ink-3">
                    PEAK TO TROUGH
                  </p>
                </div>
                <dd className="font-mono text-4xl tabular-nums text-foreground">
                  <CountUp value={maxDdPct} decimals={0} prefix="−" suffix="%" />
                </dd>
              </div>
            </dl>
            <p className="border-t border-line px-5 py-3 font-mono text-[10px] tracking-[0.14em] text-ink-3">
              NET OF COSTS ({stats.costBps} BPS/UNIT TURNOVER) · NO LEVERAGE ·
              SIGNALS LAGGED ONE DAY
            </p>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
