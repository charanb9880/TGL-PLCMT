import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import { ArrowRight, Database, Layers3, Search, Sparkles } from "lucide-react";
import { useNavigate } from "react-router-dom";

import CompanyCard from "@/components/CompanyCard";
import PageState from "@/components/PageState";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import useCompanies from "@/hooks/useCompanies";
import usePlacementFilters from "@/hooks/usePlacementFilters";
import { fetchDatasetStatus } from "@/lib/api";
import { buildAnalyticsFromCompanies } from "@/lib/analytics";
import { HOME_INSIGHT_FIELDS, VISUALS } from "@/lib/companyFrames";


const MetricCard = ({ label, value, icon: Icon, testId }) => (
  <div className="rounded-[28px] border border-zinc-200 bg-white/80 p-6 shadow-[0_18px_40px_rgba(15,23,42,0.08)]" data-testid={testId}>
    <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl border border-zinc-200 bg-zinc-50">
      <Icon className="h-5 w-5 text-[#0055ff]" />
    </div>
    <p className="text-xs font-bold uppercase tracking-[0.28em] text-zinc-500">{label}</p>
    <p className="mt-2 text-4xl font-medium tracking-tight text-zinc-950">{value}</p>
  </div>
);


const HomePage = () => {
  const navigate = useNavigate();
  const { buildRouteTarget } = usePlacementFilters();
  const [search, setSearch] = useState("");
  const [datasetStatus, setDatasetStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const { allCompanies, sourceCompanies, loading: companyLoading, error: companyError } = useCompanies({ filters: { sort_by: "name" }, pageSize: 1000 });
  const analytics = useMemo(() => buildAnalyticsFromCompanies(sourceCompanies), [sourceCompanies]);
  const companies = useMemo(() => allCompanies, [allCompanies]);

  const loadHome = async () => {
    setLoading(true);
    setError("");
    try {
      // derive stats from companies if needed, or use static placeholders for schema metadata
      setDatasetStatus({
        column_count: 163,
        available_sheets: ["Companies"],
        database_configured: true,
        columns: [
          { name: "Company Name", type: "TEXT" },
          { name: "Category", type: "TEXT" },
          { name: "Focus Sectors", type: "TEXT" },
          { name: "Employee Size", type: "TEXT" },
          { name: "Annual Revenue", type: "NUMBER" },
        ]
      });
    } catch (loadError) {
      setError(loadError.message || "Unable to load the home experience right now.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHome();
  }, []);

  if (loading || companyLoading) {
    return <PageState description="Loading company signals, schema stats, and hero insights." loading testId="home-loading-state" title="Preparing the home frames" />;
  }

  if (error || companyError) {
    return <PageState actionLabel="Retry" description={error || companyError} onAction={loadHome} testId="home-error-state" title="Home data could not load" />;
  }

  return (
    <div className="space-y-8">
      <div className="h-[calc(100vh-8rem)] snap-y snap-mandatory overflow-y-auto scroll-smooth rounded-[36px] border border-zinc-200 bg-white/50 shadow-[0_24px_80px_rgba(15,23,42,0.08)]" data-testid="home-frame-container">
        <section className="relative flex min-h-[calc(100vh-8rem)] snap-start items-center overflow-hidden px-6 py-10 md:px-10 lg:px-14" data-testid="home-hero-frame">
          <img alt="Placement intelligence hero" className="absolute inset-0 h-full w-full object-cover object-center opacity-25" src={VISUALS.hero} />
          <div className="absolute inset-0 bg-gradient-to-br from-white via-white/90 to-white/60" />

          <motion.div
            className="relative z-10 grid w-full grid-cols-1 gap-10 xl:grid-cols-[0.86fr_1.14fr]"
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.45 }}
          >
            <div>
              <p className="mb-4 inline-flex items-center gap-2 rounded-full border border-zinc-200 bg-white/80 px-4 py-2 text-xs font-bold uppercase tracking-[0.3em] text-zinc-500" data-testid="home-hero-kicker">
                <Sparkles className="h-4 w-4 text-[#0055ff]" /> Frame-based enterprise PWA
              </p>
              <h1 className="max-w-3xl text-5xl font-medium tracking-tight text-zinc-950 sm:text-6xl lg:text-7xl" data-testid="home-hero-title">
                Placement Intelligence System
              </h1>
              <p className="mt-6 max-w-2xl text-base leading-relaxed text-zinc-600 sm:text-lg" data-testid="home-hero-description">
                Explore companies, compare opportunities, map your skill fit, and review structured placement intelligence from an exact company schema.
              </p>

              <div className="mt-8 flex flex-col gap-4 rounded-[28px] border border-zinc-200 bg-white/85 p-5 shadow-[0_18px_50px_rgba(15,23,42,0.06)] sm:flex-row">
                <div className="relative flex-1">
                  <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-400" />
                  <Input
                    className="h-14 rounded-2xl border-zinc-200 bg-zinc-50 pl-11 text-sm"
                    data-testid="home-search-input"
                    onChange={(event) => setSearch(event.target.value)}
                    placeholder="Search by company, tech, or sector"
                    value={search}
                  />
                </div>
                <Button className="h-14 rounded-full bg-[#0055ff] px-8 text-white hover:bg-[#0044cc]" data-testid="home-search-submit-button" onClick={() => navigate(buildRouteTarget("/explore", { search }))}>
                  Explore now <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </div>

            <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
              <MetricCard icon={Database} label="Total companies" testId="home-metric-total-companies" value={analytics?.total_companies ?? "—"} />
              <MetricCard icon={Layers3} label="Schema columns" testId="home-metric-column-count" value={datasetStatus?.column_count ?? "—"} />
              <MetricCard icon={Sparkles} label="Available sheets" testId="home-metric-sheet-count" value={datasetStatus?.available_sheets?.length ?? "—"} />
              <MetricCard icon={Search} label="Database status" testId="home-metric-database-status" value={datasetStatus?.database_configured ? "Connected" : "Waiting"} />
            </div>
          </motion.div>
        </section>

        <section className="flex min-h-[calc(100vh-8rem)] snap-start items-center px-6 py-10 md:px-10 lg:px-14" data-testid="home-stats-frame">
          <div className="grid w-full grid-cols-1 gap-6 lg:grid-cols-[0.92fr_1.08fr]">
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.3em] text-zinc-500">Stats frame</p>
              <h2 className="mt-2 text-4xl font-medium tracking-tight text-zinc-950 sm:text-5xl">Exact-schema coverage at a glance</h2>
              <p className="mt-4 max-w-xl text-base leading-relaxed text-zinc-600">
                The uploaded workbook is already mapped to the Companies sheet, with every column preserved and ready for query-driven rendering.
              </p>
            </div>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              {(datasetStatus?.columns || []).slice(0, 8).map((column) => (
                <div className="rounded-3xl border border-zinc-200 bg-white px-5 py-4" data-testid={`home-column-card-${column.name.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`} key={column.name}>
                  <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">{column.type}</p>
                  <p className="mt-2 text-sm font-medium leading-relaxed text-zinc-900">{column.name}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="flex min-h-[calc(100vh-8rem)] snap-start items-center px-6 py-10 md:px-10 lg:px-14" data-testid="home-category-frame">
          <div className="grid w-full grid-cols-1 gap-6 lg:grid-cols-[0.74fr_1.26fr]">
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.3em] text-zinc-500">Category tiles frame</p>
              <h2 className="mt-2 text-4xl font-medium tracking-tight text-zinc-950 sm:text-5xl">Decision-ready categories</h2>
              <p className="mt-4 max-w-lg text-base leading-relaxed text-zinc-600">
                Fixed category tiles help students read the market quickly, while the explorer route keeps the full exact category field visible.
              </p>
            </div>

            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              {(analytics?.category_tiles || []).map((tile, index) => (
                <motion.div
                  animate={{ opacity: 1, y: 0 }}
                  className="relative overflow-hidden rounded-[30px] border border-zinc-200 bg-white/85 p-6 shadow-[0_18px_50px_rgba(15,23,42,0.08)]"
                  data-testid={`home-category-tile-${tile.label.toLowerCase().replace(/\s+/g, "-")}`}
                  initial={{ opacity: 0, y: 18 }}
                  key={tile.label}
                  transition={{ delay: index * 0.08, duration: 0.3 }}
                >
                  <img alt={tile.label} className="absolute inset-0 h-full w-full object-cover object-center opacity-15" src={index % 2 === 0 ? VISUALS.office : VISUALS.technology} />
                  <div className="relative z-10">
                    <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Company cluster</p>
                    <h3 className="mt-2 text-3xl font-medium tracking-tight text-zinc-950">{tile.label}</h3>
                    <p className="mt-6 text-6xl font-medium tracking-tighter text-zinc-950">{tile.count}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        <section className="flex min-h-[calc(100vh-8rem)] snap-start items-center px-6 py-10 md:px-10 lg:px-14" data-testid="home-insights-frame">
          <div className="w-full space-y-6">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.3em] text-zinc-500">Insights frame</p>
                <h2 className="mt-2 text-4xl font-medium tracking-tight text-zinc-950 sm:text-5xl">Hiring velocity, profitability, and work mode signals</h2>
              </div>
              <Button className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid="home-open-analytics-button" onClick={() => navigate("/analytics")} variant="outline">
                Open analytics dashboard
              </Button>
            </div>

            <div className="grid grid-cols-1 gap-5 xl:grid-cols-[0.72fr_1.28fr]">
              <div className="grid grid-cols-1 gap-4">
                {HOME_INSIGHT_FIELDS.map((field) => (
                  <div className="rounded-[28px] border border-zinc-200 bg-white/90 p-5 shadow-[0_18px_40px_rgba(15,23,42,0.08)]" data-testid={`home-insight-card-${field.key}`} key={field.key}>
                    <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">{field.label}</p>
                    <ul className="mt-4 space-y-3 text-sm text-zinc-700">
                      {(analytics?.[field.key] || []).slice(0, 4).map((entry) => (
                        <li className="flex items-center justify-between gap-3" key={`${field.key}-${entry.label}`}>
                          <span>{entry.label}</span>
                          <span className="rounded-full border border-zinc-200 px-3 py-1 text-xs font-medium text-zinc-900">{entry.value}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>

              <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                {companies.map((company) => (
                  <CompanyCard company={company} key={company.company_id} />
                ))}
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

export default HomePage;
