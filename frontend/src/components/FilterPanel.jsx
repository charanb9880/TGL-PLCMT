import { RefreshCcw, Search } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";


const FILTER_FIELDS = [
  { label: "Category", key: "category", source: "Category" },
  { label: "Focus Sectors / Industries", key: "focus_sectors", source: "Focus Sectors / Industries" },
  { label: "Employee Size", key: "employee_size", source: "Employee Size" },
  { label: "Profitability Status", key: "profitability_status", source: "Profitability Status" },
  { label: "Remote Work Policy", key: "remote_policy_details", source: "Remote Work Policy" },
  { label: "Hiring Velocity", key: "hiring_velocity", source: "Hiring Velocity" },
];


export default function FilterPanel({ filters = {}, values, onChange, onReset }) {
  return (
    <section className="rounded-[28px] border border-zinc-200 bg-white/85 p-6 shadow-[0_18px_50px_rgba(15,23,42,0.08)]" data-testid="company-filter-panel">
      <div className="mb-5 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.3em] text-zinc-500">Filter system</p>
          <h2 className="text-2xl font-medium tracking-tight text-zinc-950">Explore companies with exact schema fields</h2>
        </div>

        <Button className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid="company-filter-reset-button" onClick={onReset} variant="outline">
          <RefreshCcw className="mr-2 h-4 w-4" /> Reset
        </Button>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-4">
        <div className="lg:col-span-2">
          <label className="mb-2 block text-xs font-bold uppercase tracking-[0.24em] text-zinc-500" htmlFor="company-search-input">
            Search
          </label>
          <div className="relative">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-400" />
            <Input
              className="h-12 rounded-2xl border-zinc-200 bg-zinc-50 pl-10 text-sm"
              data-testid="company-search-input"
              id="company-search-input"
              onChange={(event) => onChange("search", event.target.value)}
              placeholder="Search by company, tech, or sector"
              value={values.search}
            />
          </div>
        </div>

        {FILTER_FIELDS.map((field) => (
          <div key={field.key}>
            <label className="mb-2 block text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">
              {field.label}
            </label>
            <Select onValueChange={(value) => onChange(field.key, value === "all" ? "" : value)} value={values[field.key] || "all"}>
              <SelectTrigger className="h-12 rounded-2xl border-zinc-200 bg-zinc-50 text-sm" data-testid={`filter-select-${field.key}`}>
                <SelectValue placeholder={`All ${field.label}`} />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All {field.label}</SelectItem>
                {(filters[field.source] || []).map((option) => (
                  <SelectItem key={`${field.key}-${option}`} value={option}>
                    {option}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        ))}

        <div>
          <label className="mb-2 block text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Sort by</label>
          <Select onValueChange={(value) => onChange("sort_by", value)} value={values.sort_by}>
            <SelectTrigger className="h-12 rounded-2xl border-zinc-200 bg-zinc-50 text-sm" data-testid="filter-select-sort-by">
              <SelectValue placeholder="Sort companies" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="name">Name</SelectItem>
              <SelectItem value="employee_size">Employee Size</SelectItem>
              <SelectItem value="yoy_growth_rate">Year-over-Year Growth Rate</SelectItem>
              <SelectItem value="brand_value">Brand value</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
    </section>
  );
}