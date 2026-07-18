import Reveal from "./Reveal";

export default function ReflectionSection() {
  return (
    <section id="reflection" className="border-b border-line">
      <div className="mx-auto max-w-6xl px-6 py-20 md:py-28">
        <Reveal>
          <p className="eyebrow">05 — Reflection</p>
        </Reveal>
        <Reveal delay={0.06}>
          <h2 className="mt-4 max-w-xl text-3xl font-medium tracking-tight md:text-4xl">
            What I actually learned.
          </h2>
        </Reveal>
        <Reveal delay={0.12}>
          <p className="mt-6 max-w-2xl text-sm/relaxed text-ink-2">
            The parameter sweep gave me a Sharpe of 1.11 and I almost stopped
            there — it looked great, and that was exactly the problem. Once I
            forced myself to validate out-of-sample, the real number dropped
            to something smaller and a lot noisier, and that gap taught me
            more about this strategy than the good-looking backtest ever did.
          </p>
        </Reveal>
      </div>
    </section>
  );
}
