import { X } from "lucide-react";

import { Button } from "@/components/ui/button";


const FILTER_LABELS = {
  category: "Category",
  focus_sectors: "Focus Sectors / Industries",
  employee_size: "Employee Size",
  profitability_status: "Profitability Status",
  remote_policy_details: "Remote Work Policy",
  hiring_velocity: "Hiring Velocity",
};


export default function ActiveFilterChips({ filters, onClear }) {
  const activeEntries = Object.entries(filters).filter(([key, value]) => FILTER_LABELS[key] && value);

  if (!activeEntries.length) {
    return null;
  }

  return (
    <div className="flex flex-wrap gap-3" data-testid="active-filter-chip-list">
      {activeEntries.map(([key, value]) => (
        <Button
          className="rounded-full border-zinc-300 bg-white text-zinc-800 hover:bg-zinc-100"
          data-testid={`active-filter-chip-${key}`}
          key={key}
          onClick={() => onClear(key)}
          variant="outline"
        >
          {FILTER_LABELS[key]}: {value}
          <X className="ml-2 h-3.5 w-3.5" />
        </Button>
      ))}
    </div>
  );
}