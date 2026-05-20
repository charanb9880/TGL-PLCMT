import { useEffect, useState } from "react";
import { Download } from "lucide-react";

import ActiveFilterChips from "@/components/ActiveFilterChips";
import CompanyCard from "@/components/CompanyCard";
import DataSkeleton from "@/components/DataSkeleton";
import FilterPanel from "@/components/FilterPanel";
import PageState from "@/components/PageState";
import SavedFilterPresets from "@/components/SavedFilterPresets";
import { Button } from "@/components/ui/button";
import { DEFAULT_FILTERS } from "@/context/FilterContext";
import useFilteredCompanies from "@/hooks/useFilteredCompanies";
import usePlacementFilters from "@/hooks/usePlacementFilters";
import { exportFilteredCompaniesCsv } from "@/lib/exporters";


import { getFieldValue } from "@/lib/fieldMapper";

const buildFilterOptions = (companies = []) => {
  const columns = [
    "Category",
    "Focus Sectors / Industries",
    "Employee Size",
    "Profitability Status",
    "Remote Work Policy",
    "Hiring Velocity",
  ];

  return columns.reduce((accumulator, column) => {
    accumulator[column] = [...new Set(companies.map((company) => String(getFieldValue(company, column) || "").trim()).filter(Boolean))].sort();
    return accumulator;
  }, {});
};

const ExplorePage = () => {
  const { activeFilterCount, filters, resetFilters, updateFilter, updateManyFilters } = usePlacementFilters();
  const { companies, allCompanies, sourceCompanies, loading, error } = useFilteredCompanies(filters, { pageSize: 1000 });
  const [filterOptions, setFilterOptions] = useState({});

  useEffect(() => {
    setFilterOptions(buildFilterOptions(sourceCompanies));
  }, [sourceCompanies]);

  return (
    <div className="space-y-8" data-testid="explore-page">
      <div className="max-w-3xl">
        <p className="text-xs font-bold uppercase tracking-[0.3em] text-zinc-500">Explore companies</p>
        <h1 className="mt-2 text-5xl font-medium tracking-tight text-zinc-950">Search, filter, and compare company opportunities</h1>
        <p className="mt-4 text-base leading-relaxed text-zinc-600">
          Every card and filter below is driven by exact schema fields from the company dataset, with no hardcoded company records.
        </p>
      </div>

      <FilterPanel
        filters={filterOptions}
        onChange={updateFilter}
        onReset={resetFilters}
        values={filters}
      />

      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <ActiveFilterChips filters={filters} onClear={(key) => updateFilter(key, DEFAULT_FILTERS[key])} />
        <Button className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid="explore-export-button" onClick={() => exportFilteredCompaniesCsv(allCompanies)} variant="outline">
          <Download className="mr-2 h-4 w-4" /> Export filtered company list
        </Button>
      </div>

      <SavedFilterPresets filters={filters} onApplyPreset={updateManyFilters} />

      {loading ? <DataSkeleton /> : null}
      {!loading && error ? <PageState actionLabel="Try again" description={error} onAction={resetFilters} testId="explore-error-state" title="Explore results could not load" /> : null}

      {!loading && !error ? <div className="flex items-center justify-between gap-4" data-testid="explore-results-summary">
        <p className="text-sm text-zinc-600">
          Showing <span className="font-medium text-zinc-950">{allCompanies.length}</span> companies with <span className="font-medium text-zinc-950">{activeFilterCount}</span> active filters.
        </p>
      </div> : null}

      {!loading && !error && !allCompanies.length ? <PageState actionLabel="Clear filters" description="No companies match the current decision criteria. Reset the global filters or loosen one dimension." onAction={resetFilters} testId="explore-empty-state" title="No companies match these filters" /> : null}

      {!loading && !error ? <div className="grid grid-cols-1 gap-6 md:grid-cols-2 2xl:grid-cols-3">
        {companies.map((company) => (
          <CompanyCard company={company} key={company.company_id} />
        ))}
      </div> : null}
    </div>
  );
};

export default ExplorePage;