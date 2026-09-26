import React from "react";
import { ResponsiveContainer, PieChart, Pie, Cell } from "recharts";

export function RiskScoreGauge({ score = 0, band = "low" }) {
  const normalizedScore = Math.min(100, Math.max(0, Number(score) || 0));

  const bandColors = {
    low: "#22C55E",
    medium: "#F59E0B",
    high: "#F97316",
    critical: "#EF4444",
  };

  const currentColor = bandColors[band.toLowerCase()] || bandColors.medium;

  // Gauge data: completed score vs remaining
  const data = [
    { name: "Score", value: normalizedScore },
    { name: "Remaining", value: 100 - normalizedScore },
  ];

  return (
    <div className="border border-white/20 bg-paper-dim p-6 flex flex-col justify-between">
      <div className="flex items-center justify-between border-b border-rule pb-3 mb-2">
        <span className="text-[11px] font-mono uppercase tracking-widest text-zinc-400">
          Composite Risk Assessment
        </span>
        <span
          className="text-xs font-mono font-bold uppercase px-2 py-0.5 border"
          style={{ borderColor: currentColor, color: currentColor }}
        >
          {band} Risk
        </span>
      </div>

      <div className="relative h-44 w-full flex items-center justify-center">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="75%"
              startAngle={180}
              endAngle={0}
              innerRadius={65}
              outerRadius={90}
              paddingAngle={2}
              dataKey="value"
              stroke="none"
            >
              <Cell fill={currentColor} />
              <Cell fill="rgba(255, 255, 255, 0.08)" />
            </Pie>
          </PieChart>
        </ResponsiveContainer>

        <div className="absolute top-[52%] left-1/2 -translate-x-1/2 -translate-y-1/2 text-center pointer-events-none">
          <span className="font-serif text-4xl font-bold tracking-tight text-white block">
            {normalizedScore}
          </span>
          <span className="text-[10px] font-mono text-zinc-400 uppercase tracking-widest block -mt-1">
            out of 100
          </span>
        </div>
      </div>

      {/* Risk Band Legend Scale */}
      <div className="grid grid-cols-4 gap-1 text-[10px] font-mono text-center pt-3 border-t border-rule">
        <div className="p-1 border border-green-500/20 bg-green-950/10 text-green-400">
          <span>0-25</span>
          <span className="block text-[9px] text-zinc-500">LOW</span>
        </div>
        <div className="p-1 border border-amber-500/20 bg-amber-950/10 text-amber-400">
          <span>26-50</span>
          <span className="block text-[9px] text-zinc-500">MED</span>
        </div>
        <div className="p-1 border border-orange-500/20 bg-orange-950/10 text-orange-400">
          <span>51-75</span>
          <span className="block text-[9px] text-zinc-500">HIGH</span>
        </div>
        <div className="p-1 border border-red-500/20 bg-red-950/20 text-red-400">
          <span>76-100</span>
          <span className="block text-[9px] text-zinc-500">CRIT</span>
        </div>
      </div>
    </div>
  );
}
