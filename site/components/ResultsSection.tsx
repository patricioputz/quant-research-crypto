import type { CurvePoint } from "@/lib/data";
import Reveal from "./Reveal";
import EquityCurveChart from "./EquityCurveChart";

export default function ResultsSection({ curve }: { curve: CurvePoint[] }) {
  return (
    <section id="results" className="border-b border-line">
      <div className="mx-auto max-w-6xl px-6 py-20 md:py-28">
        <Reveal>
          <p className="eyebrow">02 — Results</p>
        </Reveal>
        <Reveal delay={0.06}>
          <h2 className="mt-4 max-w-xl text-3xl font-medium tracking-tight md:text-4xl">
            Growth of $1, since 2021.
          </h2>
        </Reveal>
        <Reveal delay={0.1}>
          <p className="mt-4 max-w-2xl text-sm/relaxed text-ink-2">
            Full backtest history — fixed configuration, no re-tuning. Toggle
            series, switch to log scale to compare early-period volatility.
            The panel below the chart is the strategy&apos;s own drawdown, not
            the benchmarks&apos; — that&apos;s the number that actually
            matters for whether you could have held this.
          </p>
        </Reveal>

        <Reveal delay={0.16} className="mt-10 border border-line bg-panel/70 p-5 md:p-8">
          <EquityCurveChart data={curve} />
        </Reveal>
      </div>
    </section>
  );
}
