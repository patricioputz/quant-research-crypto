import { deflatedSharpe } from "@/data/strategy";
import Reveal from "./Reveal";

const COMMITMENTS = [
  {
    title: "No lookahead",
    body: "Every signal is computed on data available as of the prior day's close — ranking logic is lagged one day before it can act.",
  },
  {
    title: "Costs are real",
    body: "Turnover is computed explicitly; every return shown is net of 10 bps per unit of turnover, never gross.",
  },
  {
    title: "Correct annualization",
    body: "Sharpe uses √365 for crypto (trades every day) and √252 for equities (trades weekdays) — mixing these up overstates equities Sharpe by ~20%.",
  },
  {
    title: "Validated out-of-sample",
    body: "Parameters are selected on training windows only, then scored once on held-out data — rolled across 7 windows so no single lucky period drives the result.",
  },
  {
    title: "Corrected for multiple testing",
    body: `The sweep tried ${deflatedSharpe.trials} parameter combinations before picking the best. Deflated Sharpe (Bailey & López de Prado) asks: how much of that Sharpe is just the best of ${deflatedSharpe.trials} noisy draws?`,
  },
];

export default function MethodSection() {
  return (
    <section id="method" className="border-b border-line">
      <div className="mx-auto max-w-6xl px-6 py-20 md:py-28">
        <Reveal>
          <p className="eyebrow">04 — Method</p>
        </Reveal>
        <Reveal delay={0.06}>
          <h2 className="mt-4 max-w-xl text-3xl font-medium tracking-tight md:text-4xl">
            Built to be doubted.
          </h2>
        </Reveal>
        <Reveal delay={0.1}>
          <p className="mt-4 max-w-2xl text-sm/relaxed text-ink-2">
            A backtest is a machine for fooling yourself. These are the four
            commitments that keep this one honest.
          </p>
        </Reveal>

        <div className="mt-12 grid gap-px border border-line bg-line sm:grid-cols-2">
          {COMMITMENTS.map((c, i) => (
            <Reveal key={c.title} delay={0.12 + i * 0.05}>
              <div className="h-full bg-background p-6">
                <p className="font-mono text-[11px] tracking-[0.16em] text-ink-3">
                  {String(i + 1).padStart(2, "0")}
                </p>
                <h3 className="mt-3 text-base font-medium text-foreground">
                  {c.title}
                </h3>
                <p className="mt-2 text-sm/relaxed text-ink-2">{c.body}</p>
              </div>
            </Reveal>
          ))}
        </div>

        <Reveal delay={0.35}>
          <div className="mt-px border border-t-0 border-line bg-panel/70 p-6 sm:p-8">
            <p className="eyebrow">Deflated Sharpe ratio</p>
            <div className="mt-4 grid grid-cols-3 gap-6">
              <div>
                <p className="font-mono text-2xl tabular-nums text-foreground">
                  {deflatedSharpe.rawSharpe.toFixed(2)}
                </p>
                <p className="mt-1 text-xs text-ink-3">Raw in-sample Sharpe</p>
              </div>
              <div>
                <p className="font-mono text-2xl tabular-nums text-ink-2">
                  {deflatedSharpe.noiseBenchmark.toFixed(2)}
                </p>
                <p className="mt-1 text-xs text-ink-3">
                  Expected from {deflatedSharpe.trials} noisy trials
                </p>
              </div>
              <div style={{ boxShadow: "inset 2px 0 0 var(--accent)" }} className="pl-4">
                <p className="font-mono text-2xl tabular-nums text-accent">
                  {(deflatedSharpe.probability * 100).toFixed(1)}%
                </p>
                <p className="mt-1 text-xs text-ink-3">
                  Probability the edge is real, not noise
                </p>
              </div>
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
