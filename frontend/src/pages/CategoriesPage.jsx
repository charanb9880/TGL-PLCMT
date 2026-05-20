import { useMemo } from "react";
import { Download } from "lucide-react";

import ActiveFilterChips from "@/components/ActiveFilterChips";
import CompanyCard from "@/components/CompanyCard";
import DataSkeleton from "@/components/DataSkeleton";
import PageState from "@/components/PageState";
import { Button } from "@/components/ui/button";
import { DEFAULT_FILTERS } from "@/context/FilterContext";
import useFilteredCompanies from "@/hooks/useFilteredCompanies";
import usePlacementFilters from "@/hooks/usePlacementFilters";
import { exportFilteredCompaniesCsv } from "@/lib/exporters";


import { getFieldValue } from "@/lib/fieldMapper";

const CategoriesPage = () => {
  const { filters, resetFilters, updateFilter } = usePlacementFilters();
  const { allCompanies: companies, loading, error } = useFilteredCompanies(filters, { pageSize: 1000 });

  const groupedCompanies = useMemo(() => {
    return companies.reduce((groups, company) => {
      const category = getFieldValue(company, "Category") || "Uncategorized";
      const existing = groups[category] || [];
      return { ...groups, [category]: [...existing, company] };
    }, {});
  }, [companies]);

  if (loading) {
    return <DataSkeleton />;
  }

  if (error) {
    return <PageState actionLabel="Retry" description={error} onAction={resetFilters} testId="categories-error-state" title="Categories could not load" />;
  }

  return (
    <div className="space-y-10" data-testid="categories-page">
      <div className="max-w-3xl">
        <p className="text-xs font-bold uppercase tracking-[0.3em] text-zinc-500">Categories</p>
        <h1 className="mt-2 text-5xl font-medium tracking-tight text-zinc-950">Browse category clusters from the exact company field</h1>
        <p className="mt-4 text-base leading-relaxed text-zinc-600">
          This route keeps the original Category value visible while giving a denser, decision-friendly way to browse the placement landscape.
        </p>
      </div>

      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <ActiveFilterChips filters={filters} onClear={(key) => updateFilter(key, DEFAULT_FILTERS[key])} />
        <Button className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid="categories-export-button" onClick={() => exportFilteredCompaniesCsv(companies)} variant="outline">
          <Download className="mr-2 h-4 w-4" /> Export filtered company list
        </Button>
      </div>

      {!companies.length ? <PageState actionLabel="Clear filters" description="No categories match the global filter state right now." onAction={resetFilters} testId="categories-empty-state" title="No category matches found" /> : null}

      {companies.length ? Object.entries(groupedCompanies).map(([category, categoryCompanies]) => (
        <section className="space-y-5" data-testid={`category-section-${category.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`} key={category}>
          <div className="flex flex-col gap-2 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Category</p>
              <h2 className="text-3xl font-medium tracking-tight text-zinc-950">{category}</h2>
            </div>
            <p className="text-sm text-zinc-600">{categoryCompanies.length} companies</p>
          </div>

          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 2xl:grid-cols-3">
            {categoryCompanies.map((company) => (
              <CompanyCard company={company} key={`${category}-${company.company_id}`} />
            ))}
          </div>
        </section>
      )) : null}
    </div>
  );
};

export default CategoriesPage;