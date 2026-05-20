import { useEffect, useMemo, useState } from "react";
import { Copy, Download, FileText } from "lucide-react";
import { useSearchParams } from "react-router-dom";

import ComparisonTable from "@/components/ComparisonTable";
import PageState from "@/components/PageState";
import SavedComparisonWorkspaces from "@/components/SavedComparisonWorkspaces";
import { Button } from "@/components/ui/button";
import useCompanies from "@/hooks/useCompanies";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { fetchComparison } from "@/lib/api";
import { COMPARISON_SECTIONS } from "@/lib/companyFrames";
import { exportComparisonCsv, openFacultyPdfReport } from "@/lib/exporters";


const ComparePage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const { sourceCompanies: companies, loading: companiesLoading, error: companiesError } = useCompanies({ pageSize: 1000 });
  const [leftCompanyId, setLeftCompanyId] = useState(searchParams.get("c1") || searchParams.get("left") || "");
  const [rightCompanyId, setRightCompanyId] = useState(searchParams.get("c2") || searchParams.get("right") || "");
  const [comparison, setComparison] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [shareState, setShareState] = useState("");

  useEffect(() => {
    setLeftCompanyId(searchParams.get("c1") || searchParams.get("left") || "");
    setRightCompanyId(searchParams.get("c2") || searchParams.get("right") || "");
  }, [searchParams]);

  useEffect(() => {
    const params = new URLSearchParams();
    if (leftCompanyId) {
      params.set("c1", leftCompanyId);
    }
    if (rightCompanyId) {
      params.set("c2", rightCompanyId);
    }
    if (params.toString() !== searchParams.toString()) {
      setSearchParams(params, { replace: true });
    }
  }, [leftCompanyId, rightCompanyId]);

  const runComparison = async () => {
    if (!leftCompanyId || !rightCompanyId) {
      return;
    }

    setLoading(true);
    setError("");
    try {
      const data = await fetchComparison(leftCompanyId, rightCompanyId);
      setComparison(data);
    } catch (loadError) {
      setError(loadError.message || "Comparison could not be generated right now.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (leftCompanyId && rightCompanyId) {
      runComparison();
      return;
    }
    setComparison(null);
  }, [leftCompanyId, rightCompanyId]);

  const shareUrl = useMemo(() => {
    if (!leftCompanyId || !rightCompanyId) {
      return "";
    }
    return `${window.location.origin}/compare?c1=${encodeURIComponent(leftCompanyId)}&c2=${encodeURIComponent(rightCompanyId)}`;
  }, [leftCompanyId, rightCompanyId]);

  const handleShareLink = async () => {
    if (!shareUrl) {
      return;
    }

    try {
      await navigator.clipboard.writeText(shareUrl);
      setShareState("Comparison link copied.");
      return;
    } catch {
      const tempInput = document.createElement("textarea");
      tempInput.value = shareUrl;
      tempInput.setAttribute("readonly", "true");
      tempInput.style.position = "absolute";
      tempInput.style.left = "-9999px";
      document.body.appendChild(tempInput);
      tempInput.select();
      const copied = document.execCommand("copy");
      document.body.removeChild(tempInput);
      setShareState(copied ? "Comparison link copied." : `Share this link: ${shareUrl}`);
    }
  };

  return (
    <div className="space-y-8" data-testid="compare-page">
      <div className="max-w-3xl">
        <p className="text-xs font-bold uppercase tracking-[0.3em] text-zinc-500">Compare</p>
        <h1 className="mt-2 text-5xl font-medium tracking-tight text-zinc-950">Side-by-side company comparison</h1>
        <p className="mt-4 text-base leading-relaxed text-zinc-600">
          Compare culture, compensation, learning, financials, and technology using the exact company schema and rule-based strengths / weaknesses / risks.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-5 rounded-[28px] border border-zinc-200 bg-white/90 p-6 shadow-[0_18px_50px_rgba(15,23,42,0.08)] xl:grid-cols-[1fr_1fr_auto]" data-testid="compare-controls-panel">
        <div>
          <label className="mb-2 block text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Left company</label>
          <Select onValueChange={setLeftCompanyId} value={leftCompanyId}>
            <SelectTrigger className="h-12 rounded-2xl border-zinc-200 bg-zinc-50" data-testid="compare-left-company-select">
              <SelectValue placeholder="Select left company" />
            </SelectTrigger>
            <SelectContent>
              {companies.map((company) => (
                <SelectItem key={`left-${company.company_id}`} value={String(company.company_id)}>
                  {company["Company Name"]}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div>
          <label className="mb-2 block text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Right company</label>
          <Select onValueChange={setRightCompanyId} value={rightCompanyId}>
            <SelectTrigger className="h-12 rounded-2xl border-zinc-200 bg-zinc-50" data-testid="compare-right-company-select">
              <SelectValue placeholder="Select right company" />
            </SelectTrigger>
            <SelectContent>
              {companies.map((company) => (
                <SelectItem key={`right-${company.company_id}`} value={String(company.company_id)}>
                  {company["Company Name"]}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="flex items-end">
          <Button className="h-12 rounded-full bg-[#0055ff] px-8 text-white hover:bg-[#0044cc]" data-testid="compare-run-button" disabled={!leftCompanyId || !rightCompanyId} onClick={runComparison}>
            Compare
          </Button>
        </div>
      </div>

      <div className="flex flex-wrap gap-3" data-testid="compare-action-row">
        <Button className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid="compare-share-link-button" disabled={!shareUrl} onClick={handleShareLink} variant="outline">
          <Copy className="mr-2 h-4 w-4" /> Share comparison link
        </Button>
        <Button className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid="compare-export-button" disabled={!comparison} onClick={() => exportComparisonCsv(comparison, COMPARISON_SECTIONS)} variant="outline">
          <Download className="mr-2 h-4 w-4" /> Export comparison CSV
        </Button>
        <Button className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid="compare-pdf-export-button" disabled={!comparison} onClick={() => openFacultyPdfReport({ title: "Comparison Report", description: "Print-ready comparison for faculty review.", companies: [comparison?.left_company, comparison?.right_company].filter(Boolean), comparison })} variant="outline">
          <FileText className="mr-2 h-4 w-4" /> Export PDF
        </Button>
      </div>

      {shareState ? <p className="text-sm text-zinc-600" data-testid="compare-share-state">{shareState}</p> : null}

      {loading && !comparison ? <PageState description="Loading company options for comparison." loading testId="compare-loading-state" title="Preparing compare mode" /> : null}
      {companiesLoading && !comparison ? <PageState description="Loading company options for comparison." loading testId="compare-loading-state" title="Preparing compare mode" /> : null}
      {!companiesLoading && (error || companiesError) ? <PageState actionLabel="Retry" description={error || companiesError} onAction={runComparison} testId="compare-error-state" title="Comparison is unavailable" /> : null}

      <SavedComparisonWorkspaces comparison={comparison} leftCompanyId={leftCompanyId} onLoadWorkspace={(workspace) => {
        setLeftCompanyId(String(workspace.leftCompanyId));
        setRightCompanyId(String(workspace.rightCompanyId));
        setSearchParams({ c1: String(workspace.leftCompanyId), c2: String(workspace.rightCompanyId) });
        setComparison(workspace.comparison);
      }} rightCompanyId={rightCompanyId} />

      <ComparisonTable comparison={comparison} />
    </div>
  );
}

export default ComparePage;
