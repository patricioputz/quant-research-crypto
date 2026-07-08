export default function Nav() {
  return (
    <header className="sticky top-0 z-50 border-b border-line bg-background/85 backdrop-blur-sm">
      <div className="mx-auto flex h-12 max-w-6xl items-center justify-between px-6">
        <a
          href="#top"
          className="font-mono text-[11px] tracking-[0.18em] text-ink-2 transition-colors hover:text-foreground"
        >
          <span className="text-accent">QR—001</span>
          <span className="mx-2 text-ink-3">/</span>
          CROSS-SECTIONAL MOMENTUM
        </a>
        <nav className="hidden gap-7 font-mono text-[11px] tracking-[0.18em] text-ink-3 sm:flex">
          <a className="transition-colors hover:text-foreground" href="#strategy">
            01 STRATEGY
          </a>
          <a className="transition-colors hover:text-foreground" href="#results">
            02 RESULTS
          </a>
          <a className="transition-colors hover:text-foreground" href="#numbers">
            03 NUMBERS
          </a>
          <a className="transition-colors hover:text-foreground" href="#method">
            04 METHOD
          </a>
          <a className="transition-colors hover:text-foreground" href="#reflection">
            05 REFLECTION
          </a>
        </nav>
      </div>
    </header>
  );
}
