import { useEffect, useMemo, useState } from "react";
import { ArrowRight, FileDown } from "lucide-react";

import ActiveFilterChips from "@/components/ActiveFilterChips";
import AnalyticsCharts from "@/components/AnalyticsCharts";
import PageState from "@/components/PageState";
import SavedFilterPresets from "@/components/SavedFilterPresets";
import SavedDashboards from "@/components/SavedDashboards";
import { Button } from "@/components/ui/button";
import { DEFAULT_FILTERS } from "@/context/FilterContext";
import useFilteredCompanies from "@/hooks/useFilteredCompanies";
import usePlacementFilters from "@/hooks/usePlacementFilters";
import { fetchDatasetStatus } from "@/lib/api";
import { buildAnalyticsFromCompanies } from "@/lib/analytics";
import { exportFacultyBriefingCsv, openFacultyPdfReport } from "@/lib/exporters";


const AnalyticsPage = () => {
  const { buildRouteTarget, filters, updateFilter, updateManyFilters } = usePlacementFilters();
  const { allCompanies: companies, loading: companiesLoading, error: companiesError } = useFilteredCompanies(filters, { pageSize: 1000 });
  const [datasetStatus, setDatasetStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadAnalytics = async () => {
    setLoading(true);
    setError("");
    try {
      const datasetData = await fetchDatasetStatus();
      setDatasetStatus(datasetData);
    } catch (loadError) {
      setError(loadError.message || "Unable to load analytics right now.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const dashboardId = params.get("dashboard");
    if (!dashboardId) {
      return;
    }
    const dashboards = JSON.parse(window.localStorage.getItem("placement-saved-dashboards-v1") || "[]");
    const dashboard = dashboards.find((item) => String(item.id) === dashboardId);
    if (dashboard?.filters) {
      updateManyFilters(dashboard.filters);
    }
  }, []);

  const analytics = useMemo(() => buildAnalyticsFromCompanies(companies), [companies]);

  const handleFilterSelect = (key, value) => {
    updateFilter(key, filters[key] === value ? DEFAULT_FILTERS[key] : value);
  };

  if (loading || companiesLoading) {
    return <PageState description="Loading category, hiring, profitability, and work mode analytics." loading testId="analytics-loading-state" title="Preparing analytics" />;
  }

  if (error || companiesError) {
    return <PageState actionLabel="Retry" description={error || companiesError} onAction={loadAnalytics} testId="analytics-error-state" title="Analytics could not load" />;
  }

  return (
    <div className="space-y-8" data-testid="analytics-page">
      <div className="grid grid-cols-1 gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.3em] text-zinc-500">Analytics</p>
          <h1 className="mt-2 text-5xl font-medium tracking-tight text-zinc-950">Placement intelligence analytics dashboard</h1>
          <p className="mt-4 text-base leading-relaxed text-zinc-600">
            Review category distribution, hiring velocity, profitability mix, and work mode exposure through a clean enterprise analytics surface.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div className="rounded-[28px] border border-zinc-200 bg-white/90 p-5 shadow-[0_18px_40px_rgba(15,23,42,0.08)]" data-testid="analytics-total-companies-card">
            <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Total companies</p>
            <p className="mt-2 text-4xl font-medium tracking-tight text-zinc-950">{analytics?.total_companies ?? "—"}</p>
          </div>
          <div className="rounded-[28px] border border-zinc-200 bg-white/90 p-5 shadow-[0_18px_40px_rgba(15,23,42,0.08)]" data-testid="analytics-columns-card">
            <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Columns mapped</p>
            <p className="mt-2 text-4xl font-medium tracking-tight text-zinc-950">{datasetStatus?.column_count ?? "—"}</p>
          </div>
          <div className="rounded-[28px] border border-zinc-200 bg-white/90 p-5 shadow-[0_18px_40px_rgba(15,23,42,0.08)]" data-testid="analytics-sheet-card">
            <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Sheets discovered</p>
            <p className="mt-2 text-4xl font-medium tracking-tight text-zinc-950">{datasetStatus?.available_sheets?.length ?? "—"}</p>
          </div>
        </div>
      </div>

      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <ActiveFilterChips filters={filters} onClear={(key) => updateFilter(key, DEFAULT_FILTERS[key])} />
        <div className="flex flex-wrap gap-3">
          <Button asChild className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid="analytics-open-filtered-explore-button" variant="outline">
            <a href={buildRouteTarget("/explore")}>
              Open filtered explorer <ArrowRight className="ml-2 h-4 w-4" />
            </a>
          </Button>
          <Button className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid="analytics-briefing-export-button" onClick={() => {
            const workspaces = JSON.parse(window.localStorage.getItem("placement-comparison-workspaces-v1") || "[]");
            exportFacultyBriefingCsv({ analytics, companies, comparison: workspaces[0]?.comparison || null });
          }} variant="outline">
            <FileDown className="mr-2 h-4 w-4" /> Export faculty briefing pack
          </Button>
          <Button className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid="analytics-pdf-export-button" onClick={() => {
            const workspaces = JSON.parse(window.localStorage.getItem("placement-comparison-workspaces-v1") || "[]");
            openFacultyPdfReport({ title: "Faculty Analytics Briefing", description: "Print-ready placement intelligence summary.", analytics, companies, comparison: workspaces[0]?.comparison || null });
          }} variant="outline">
            <FileDown className="mr-2 h-4 w-4" /> Export PDF
          </Button>
        </div>
      </div>

      <SavedFilterPresets filters={filters} onApplyPreset={updateManyFilters} />
      <SavedDashboards buildDashboardUrl={(dashboardFilters, dashboardId) => `${buildRouteTarget("/analytics", dashboardFilters)}${buildRouteTarget("/analytics", dashboardFilters).includes("?") ? "&" : "?"}dashboard=${dashboardId}`} filters={filters} onApplyDashboard={(dashboard) => updateManyFilters(dashboard.filters)} />

      <AnalyticsCharts activeFilters={filters} analytics={analytics} onFilterSelect={handleFilterSelect} />
    </div>
  );
}

export default AnalyticsPage;
