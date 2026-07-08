import fs from "node:fs";
import path from "node:path";

export type CurvePoint = {
  t: number; // unix ms, UTC midnight
  strategy: number; // growth of $1
  cryptoEw: number;
  spy: number;
  drawdown: number; // strategy drawdown as a fraction (<= 0)
};

export function loadEquityCurve(): CurvePoint[] {
  const file = path.join(process.cwd(), "data", "equity-curve.csv");
  const raw = fs.readFileSync(file, "utf8").trim();
  const [, ...rows] = raw.split("\n");
  return rows.map((line) => {
    const [date, strategy, cryptoEw, spy, drawdown] = line.split(",");
    return {
      t: Date.parse(`${date}T00:00:00Z`),
      strategy: Number(strategy),
      cryptoEw: Number(cryptoEw),
      spy: Number(spy),
      drawdown: Number(drawdown),
    };
  });
}
