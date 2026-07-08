import { strategy } from "@/data/strategy";

export default function Footer() {
  return (
    <footer className="mx-auto max-w-6xl px-6 py-10">
      <div className="flex flex-col items-start justify-between gap-4 text-sm text-ink-3 sm:flex-row sm:items-center">
        <p>{strategy.author}</p>
        <p className="font-mono text-[11px] tracking-[0.14em]">
          EVERY NUMBER HERE IS BUILT TO BE DOUBTED.
        </p>
        <a
          href={strategy.github}
          target="_blank"
          rel="noopener noreferrer"
          className="font-mono text-[11px] tracking-[0.14em] transition-colors hover:text-foreground"
        >
          GITHUB ↗
        </a>
      </div>
    </footer>
  );
}
