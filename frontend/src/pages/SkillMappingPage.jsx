import { useState } from "react";

import PageState from "@/components/PageState";
import SkillMatchPanel from "@/components/SkillMatchPanel";
import useCompanies from "@/hooks/useCompanies";
import { runSkillMatch } from "@/lib/api";


const SkillMappingPage = () => {
  const { allCompanies: companies, loading: pageLoading, error: companiesError } = useCompanies({ filters: { sort_by: "brand_value" }, pageSize: 1000 });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRunSkillMatch = async (payload) => {
    setLoading(true);
    setError("");
    try {
      const data = await runSkillMatch(payload);
      setResult(data);
    } catch (loadError) {
      setError(loadError.message || "Skill mapping could not be generated right now.");
    } finally {
      setLoading(false);
    }
  };

  if (pageLoading) {
    return <PageState description="Loading companies for rule-based skill matching." loading testId="skill-mapping-loading-state" title="Preparing skill mapping" />;
  }

  if ((error || companiesError) && !loading && !companies.length) {
    return <PageState actionLabel="Retry" description={error || companiesError} onAction={() => window.location.reload()} testId="skill-mapping-error-state" title="Skill mapping is unavailable" />;
  }

  return (
    <div className="space-y-8" data-testid="skill-mapping-page">
      <div className="max-w-3xl">
        <p className="text-xs font-bold uppercase tracking-[0.3em] text-zinc-500">Skill mapping</p>
        <h1 className="mt-2 text-5xl font-medium tracking-tight text-zinc-950">Rule-based fit, gap, and preparation mapping</h1>
        <p className="mt-4 text-base leading-relaxed text-zinc-600">
          Enter your skills manually and match them against exact company fields without using AI generation — only rule-based evaluation.
        </p>
      </div>

      {error && companies.length ? (
        <div className="rounded-[24px] border border-amber-200 bg-amber-50 px-5 py-4 text-sm text-amber-800" data-testid="skill-mapping-inline-error">
          {error}
        </div>
      ) : null}

      <SkillMatchPanel companies={companies} loading={loading} onRun={handleRunSkillMatch} result={result} />
    </div>
  );
}

export default SkillMappingPage;
