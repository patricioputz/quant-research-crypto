"use client";

import { useMemo, useState } from "react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  Line,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { CurvePoint } from "@/lib/data";

type SeriesKey = "strategy" | "cryptoEw" | "spy";

const SERIES: { key: SeriesKey; label: string; color: string; dashed?: boolean }[] = [
  { key: "strategy", label: "Strategy", color: "var(--accent)" },
  { key: "cryptoEw", label: "Equal-Weight Crypto", color: "var(--ink-2)" },
  { key: "spy", label: "SPY", color: "var(--ink-3)", dashed: true },
];

function formatDate(t: number) {
  return new Date(t).toLocaleDateString("en-US", { year: "numeric", month: "short" });
}

function CurveTooltip({
  active,
  payload,
  label,
}: {
  active?: boolean;
  payload?: { dataKey: string; value: number }[];
  label?: number;
}) {
  if (!active || !payload?.length) return null;
  const byKey = Object.fromEntries(payload.map((p) => [p.dataKey, p.value]));
  return (
    <div className="border border-line bg-panel px-4 py-3 text-sm shadow-lg">
      <p className="eyebrow mb-2">{label ? formatDate(label) : ""}</p>
      {SERIES.filter((s) => byKey[s.key] !== undefined).map((s) => (
        <div key={s.key} className="flex items-center justify-between gap-6 py-0.5">
          <span className="flex items-center gap-2 text-ink-2">
            <span
              className="inline-block h-2 w-2 rounded-full"
              style={{ background: s.color }}
            />
            {s.label}
          </span>
          <span className="font-mono tabular-nums text-foreground">
            {`${Number(byKey[s.key]).toFixed(2)}x`}
          </span>
        </div>
      ))}
    </div>
  );
}

export default function EquityCurveChart({ data }: { data: CurvePoint[] }) {
  const [visible, setVisible] = useState<Record<SeriesKey, boolean>>({
    strategy: true,
    cryptoEw: true,
    spy: true,
  });
  const [logScale, setLogScale] = useState(false);

  const chartData = useMemo(
    () => data.map((d) => ({ ...d, drawdownPct: d.drawdown * 100 })),
    [data]
  );
  const maxDrawdownPct = useMemo(
    () => Math.min(...chartData.map((d) => d.drawdownPct)),
    [chartData]
  );

  return (
    <div>
      <div className="mb-4 flex flex-wrap items-center justify-between gap-4">
        <div className="flex flex-wrap gap-4">
          {SERIES.map((s) => (
            <button
              key={s.key}
              onClick={() =>
                setVisible((v) => ({ ...v, [s.key]: !v[s.key] }))
              }
              className="flex items-center gap-2 font-mono text-[11px] tracking-[0.1em] transition-opacity"
              style={{ opacity: visible[s.key] ? 1 : 0.35 }}
            >
              <span
                className="inline-block h-2.5 w-2.5 rounded-full"
                style={{ background: s.color }}
              />
              <span className="text-ink-2">{s.label.toUpperCase()}</span>
            </button>
          ))}
        </div>
        <button
          onClick={() => setLogScale((v) => !v)}
          className="border border-line px-2.5 py-1 font-mono text-[11px] tracking-[0.1em] text-ink-2 transition-colors hover:text-foreground"
        >
          {logScale ? "LOG" : "LINEAR"}
        </button>
      </div>

      <div className="h-[360px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 4, right: 8, bottom: 0, left: 0 }}>
            <defs>
              <linearGradient id="strategyFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="var(--accent)" stopOpacity={0.14} />
                <stop offset="100%" stopColor="var(--accent)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="var(--line)" strokeDasharray="0" vertical={false} />
            <XAxis
              dataKey="t"
              type="number"
              domain={["dataMin", "dataMax"]}
              tickFormatter={formatDate}
              stroke="var(--line)"
              tick={{ fill: "var(--ink-3)", fontSize: 11 }}
              tickLine={false}
              minTickGap={60}
            />
            <YAxis
              scale={logScale ? "log" : "linear"}
              domain={logScale ? ["auto", "auto"] : [0, "auto"]}
              stroke="var(--line)"
              tick={{ fill: "var(--ink-3)", fontSize: 11 }}
              tickLine={false}
              tickFormatter={(v: number) => `${v.toFixed(1)}x`}
              width={44}
            />
            <Tooltip content={<CurveTooltip />} />
            {visible.cryptoEw && (
              <Line
                type="monotone"
                dataKey="cryptoEw"
                stroke="var(--ink-2)"
                strokeWidth={1.5}
                dot={false}
                isAnimationActive={false}
              />
            )}
            {visible.spy && (
              <Line
                type="monotone"
                dataKey="spy"
                stroke="var(--ink-3)"
                strokeWidth={1.5}
                strokeDasharray="4 3"
                dot={false}
                isAnimationActive={false}
              />
            )}
            {visible.strategy && (
              <Area
                type="monotone"
                dataKey="strategy"
                stroke="var(--accent)"
                strokeWidth={2}
                fill="url(#strategyFill)"
                dot={false}
                isAnimationActive={false}
              />
            )}
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-2 h-[100px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 8, right: 8, bottom: 0, left: 0 }}>
            <defs>
              <linearGradient id="ddFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="var(--ink-3)" stopOpacity={0} />
                <stop offset="100%" stopColor="var(--ink-3)" stopOpacity={0.25} />
              </linearGradient>
            </defs>
            <XAxis dataKey="t" type="number" domain={["dataMin", "dataMax"]} hide />
            <YAxis
              domain={["auto", 0]}
              stroke="var(--line)"
              tick={{ fill: "var(--ink-3)", fontSize: 10 }}
              tickLine={false}
              tickFormatter={(v: number) => `${v.toFixed(0)}%`}
              width={44}
            />
            <Tooltip
              content={({ active, payload, label }) =>
                active && payload?.length ? (
                  <div className="border border-line bg-panel px-3 py-2 text-xs">
                    <p className="eyebrow mb-1">{label ? formatDate(label as number) : ""}</p>
                    <p className="font-mono text-ink-2">
                      Drawdown {Number(payload[0].value).toFixed(1)}%
                    </p>
                  </div>
                ) : null
              }
            />
            <ReferenceLine
              y={maxDrawdownPct}
              stroke="var(--ink-3)"
              strokeDasharray="3 3"
              label={{
                value: `MAX ${maxDrawdownPct.toFixed(1)}%`,
                position: "insideBottomRight",
                fill: "var(--ink-3)",
                fontSize: 10,
                fontFamily: "var(--font-geist-mono)",
              }}
            />
            <Area
              type="monotone"
              dataKey="drawdownPct"
              stroke="var(--ink-3)"
              strokeWidth={1}
              fill="url(#ddFill)"
              isAnimationActive={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
      <p className="mt-1 eyebrow">Strategy drawdown</p>
    </div>
  );
}
