import { strategy, walkForwardWindows, crossAsset } from "@/data/strategy";
import Reveal from "./Reveal";

function StatRow({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return (
    <div className="flex items-baseline justify-between border-b border-line py-4 last:border-none">
      <div>
        <p className="text-sm text-foreground">{label}</p>
        {sub && <p className="mt-0.5 text-xs text-ink-3">{sub}</p>}
      </div>
      <p className="font-mono text-lg text-foreground">{value}</p>
    </div>
  );
}

export default function NumbersSection() {
  const { stats } = strategy;

  return (
    <section id="numbers" className="border-b border-line">
      <div className="mx-auto max-w-6xl px-6 py-20 md:py-28">
        <Reveal>
          <p className="eyebrow">03 — The Numbers</p>
        </Reveal>
        <Reveal delay={0.06}>
          <h2 className="mt-4 max-w-2xl text-3xl font-medium tracking-tight md:text-4xl">
            The honest number is smaller than the headline one.
          </h2>
        </Reveal>
        <Reveal delay={0.1}>
          <p className="mt-4 max-w-2xl text-sm/relaxed text-ink-2">
            {strategy.finding}
          </p>
        </Reveal>

        <div className="mt-12 grid gap-10 md:grid-cols-2">
          <Reveal delay={0.12}>
            <p className="eyebrow mb-2">Fixed config, full history</p>
            <div>
              <StatRow label="Sharpe" value={stats.sharpe.toFixed(2)} />
              <StatRow label="Max drawdown" value={`${(stats.maxDrawdown * 100).toFixed(0)}%`} />
              <StatRow label="Lookback" value={`${stats.lookbackDays}d`} />
              <StatRow label="Rebalance" value={`${stats.holdDays}d`} />
            </div>
          </Reveal>

          <Reveal delay={0.18}>
            <p className="eyebrow mb-2">Rolling walk-forward, 7 windows (2021–2024)</p>
            <div>
              <StatRow
                label="Avg out-of-sample Sharpe"
                value={stats.oosSharpeAvg.toFixed(2)}
                sub="each window treated as one data point"
              />
              <StatRow
                label="Stitched out-of-sample Sharpe"
                value={stats.oosSharpeStitched.toFixed(2)}
                sub="continuous daily P&L across all windows"
              />
              <StatRow label="Out-of-sample max drawdown" value={`${(stats.oosMaxDrawdown * 100).toFixed(0)}%`} />
            </div>
          </Reveal>
        </div>

        <Reveal delay={0.2} className="mt-14">
          <p className="eyebrow mb-3">Per-window detail</p>
          <div className="overflow-x-auto border border-line">
            <table className="w-full min-w-[560px] text-sm">
              <thead>
                <tr className="border-b border-line text-left">
                  <th className="px-4 py-2.5 font-normal text-ink-3">Window</th>
                  <th className="px-4 py-2.5 font-normal text-ink-3">Lookback</th>
                  <th className="px-4 py-2.5 font-normal text-ink-3">Hold</th>
                  <th className="px-4 py-2.5 text-right font-normal text-ink-3">Train Sharpe</th>
                  <th className="px-4 py-2.5 text-right font-normal text-ink-3">Test Sharpe</th>
                </tr>
              </thead>
              <tbody className="font-mono">
                {walkForwardWindows.map((w) => (
                  <tr key={w.windowStart} className="border-b border-line/60 last:border-none">
                    <td className="px-4 py-2.5 text-ink-2">{w.windowStart}</td>
                    <td className="px-4 py-2.5 text-ink-2">{w.lookback}d</td>
                    <td className="px-4 py-2.5 text-ink-2">{w.hold}d</td>
                    <td className="px-4 py-2.5 text-right text-ink-2">{w.trainSharpe.toFixed(2)}</td>
                    <td
                      className="px-4 py-2.5 text-right"
                      style={{ color: w.testSharpe >= 0 ? "var(--accent)" : "var(--ink-3)" }}
                    >
                      {w.testSharpe.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Reveal>

        <Reveal delay={0.24} className="mt-14">
          <p className="eyebrow mb-3">Cross-asset check — same signal on 50 equities</p>
          <p className="max-w-2xl text-sm/relaxed text-ink-2">
            Running the crypto-tuned parameters unchanged on equities gave
            Sharpe <span className="font-mono text-foreground">{crossAsset.naiveSharpe.toFixed(2)}</span> —
            crypto-speed parameters sit in equities&apos; short-term reversal
            zone, not its momentum zone. Re-tuned to a{" "}
            {crossAsset.tunedLookback}-day lookback /{" "}
            {crossAsset.tunedHold}-day hold (3–12 month horizon, standard for
            equities momentum), Sharpe flips to{" "}
            <span className="font-mono text-accent">{crossAsset.tunedSharpe.toFixed(2)}</span> —
            still trails equal-weight buy-and-hold ({crossAsset.equityBuyHoldSharpe.toFixed(2)}),
            since a market-neutral book gives up the beta a bull market pays for.
          </p>
        </Reveal>
      </div>
    </section>
  );
}
