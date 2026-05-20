import { useEffect, useRef, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ANALYTICS_SECTIONS } from "@/lib/companyFrames";
import { buildChartPalette } from "@/lib/formatters";
import { ANALYTICS_FILTER_MAP } from "@/lib/analytics";


const palette = buildChartPalette();


function ChartViewport({ children, testId }) {
  const ref = useRef(null);
  const [size, setSize] = useState({ width: 0, height: 0 });

  useEffect(() => {
    const element = ref.current;
    if (!element) {
      return undefined;
    }

    const observer = new ResizeObserver(([entry]) => {
      setSize({ width: entry.contentRect.width, height: entry.contentRect.height });
    });

    observer.observe(element);
    return () => observer.disconnect();
  }, []);

  return (
    <div className="h-72 min-w-0" data-testid={testId} ref={ref}>
      {size.width > 40 && size.height > 40 ? children(size) : <div className="flex h-full items-center justify-center text-sm text-zinc-400">Preparing chart…</div>}
    </div>
  );
}


export default function AnalyticsCharts({ activeFilters, analytics, onFilterSelect }) {
  if (!analytics) {
    return null;
  }

  const readChartLabel = (entry) => entry?.label || entry?.payload?.label || entry?.activeLabel;

  return (
    <div className="grid grid-cols-1 gap-6 xl:grid-cols-2" data-testid="analytics-charts-grid">
      {ANALYTICS_SECTIONS.map((section, index) => {
        const chartData = (analytics[section.key] || []).slice(0, 6).map((entry) => ({
          ...entry,
          shortLabel: entry.label.length > 14 ? `${entry.label.slice(0, 14)}…` : entry.label,
        }));

        const filterKey = ANALYTICS_FILTER_MAP[section.key];

        return (
        <Card className="rounded-[28px] border-zinc-200 bg-white/90 shadow-[0_18px_50px_rgba(15,23,42,0.08)]" data-testid={`analytics-card-${section.key}`} key={section.key}>
          <CardContent className="space-y-6 p-6">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl border border-zinc-200 bg-zinc-50">
                <section.icon className="h-5 w-5 text-[#0055ff]" />
              </div>
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.28em] text-zinc-500">Analytics</p>
                <h3 className="text-2xl font-medium tracking-tight text-zinc-950">{section.title}</h3>
              </div>
            </div>

            {filterKey ? (
              <div className="flex flex-wrap gap-3" data-testid={`analytics-filter-controls-${section.key}`}>
                {chartData.slice(0, 5).map((entry) => {
                  const active = activeFilters?.[filterKey] === entry.label;
                  return (
                    <Button
                      className={`rounded-full border px-4 py-2 text-sm ${active ? "border-zinc-900 bg-zinc-950 text-white" : "border-zinc-300 bg-white text-zinc-800 hover:bg-zinc-100"}`}
                      data-testid={`analytics-filter-chip-${section.key}-${entry.label.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}
                      key={`${section.key}-${entry.label}`}
                      onClick={() => onFilterSelect(filterKey, entry.label)}
                      variant="outline"
                    >
                      {entry.label} · {entry.value}
                    </Button>
                  );
                })}
              </div>
            ) : null}

            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              <ChartViewport testId={`analytics-pie-${section.key}`}>
                {({ width, height }) => (
                  <PieChart height={height} width={width}>
                    <Pie data={chartData} dataKey="value" nameKey="label" onClick={(entry) => filterKey && onFilterSelect(filterKey, readChartLabel(entry))} outerRadius={92} innerRadius={52}>
                      {chartData.map((entry, entryIndex) => (
                        <Cell fill={palette[entryIndex % palette.length]} key={`${entry.label}-${entryIndex}`} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                )}
              </ChartViewport>

              <ChartViewport testId={`analytics-bar-${section.key}`}>
                {({ width, height }) => (
                  <BarChart data={chartData} height={height} margin={{ top: 16, right: 8, left: -12, bottom: 32 }} width={width}>
                    <CartesianGrid stroke="#ececf0" vertical={false} />
                    <XAxis angle={-18} dataKey="shortLabel" interval={0} textAnchor="end" tick={{ fill: "#71717a", fontSize: 11 }} />
                    <YAxis tick={{ fill: "#71717a", fontSize: 12 }} />
                    <Tooltip />
                    <Bar dataKey="value" fill={palette[index % palette.length]} onClick={(entry) => filterKey && onFilterSelect(filterKey, readChartLabel(entry))} radius={[8, 8, 0, 0]} />
                  </BarChart>
                )}
              </ChartViewport>
            </div>
          </CardContent>
        </Card>
      )})}
    </div>
  );
}