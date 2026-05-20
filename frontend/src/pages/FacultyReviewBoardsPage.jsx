import { useEffect, useMemo, useState } from "react";
import { FileDown, FolderPlus, Trash2 } from "lucide-react";

import ActiveFilterChips from "@/components/ActiveFilterChips";
import PageState from "@/components/PageState";
import { Button } from "@/components/ui/button";
import { DEFAULT_FILTERS } from "@/context/FilterContext";
import useCompanies from "@/hooks/useCompanies";
import useFilteredCompanies from "@/hooks/useFilteredCompanies";
import usePlacementFilters from "@/hooks/usePlacementFilters";
import { buildAnalyticsFromCompanies } from "@/lib/analytics";
import { exportFacultyBriefingCsv, openFacultyPdfReport } from "@/lib/exporters";


const STORAGE_KEY = "faculty-review-boards-v1";


const FacultyReviewBoardsPage = () => {
  const { filters, updateFilter } = usePlacementFilters();
  const { sourceCompanies, loading, error } = useCompanies({ pageSize: 1000 });
  const { allCompanies: filteredCompanies } = useFilteredCompanies(filters, { pageSize: 1000 });
  const [boards, setBoards] = useState([]);
  const [selectedCompanyIds, setSelectedCompanyIds] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  useEffect(() => {
    setBoards(JSON.parse(window.localStorage.getItem(STORAGE_KEY) || "[]"));
  }, []);

  const companyMap = useMemo(
    () => new Map(sourceCompanies.map((company) => [String(company.company_id), company])),
    [sourceCompanies],
  );

  const toggleCompany = (companyId) => {
    setSelectedCompanyIds((previous) =>
      previous.includes(companyId)
        ? previous.filter((id) => id !== companyId)
        : [...previous, companyId],
    );
  };

  const saveBoard = () => {
    if (!name.trim() || !selectedCompanyIds.length) {
      return;
    }

    const nextBoards = [
      {
        id: Date.now(),
        name: name.trim(),
        description: description.trim(),
        companyIds: selectedCompanyIds,
      },
      ...boards,
    ];
    setBoards(nextBoards);
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(nextBoards));
    setName("");
    setDescription("");
    setSelectedCompanyIds([]);
  };

  const deleteBoard = (boardId) => {
    const nextBoards = boards.filter((board) => board.id !== boardId);
    setBoards(nextBoards);
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(nextBoards));
  };

  if (loading) {
    return <PageState description="Loading filtered companies for faculty board creation." loading testId="faculty-review-boards-loading-state" title="Preparing review boards" />;
  }

  if (error) {
    return <PageState actionLabel="Retry" description={error} onAction={() => window.location.reload()} testId="faculty-review-boards-error-state" title="Faculty review boards could not load" />;
  }

  return (
    <div className="space-y-8" data-testid="faculty-review-boards-page">
      <div className="max-w-3xl">
        <p className="text-xs font-bold uppercase tracking-[0.3em] text-zinc-500">Faculty review boards</p>
        <h1 className="mt-2 text-5xl font-medium tracking-tight text-zinc-950">Build shortlisting boards for placement panels</h1>
        <p className="mt-4 text-base leading-relaxed text-zinc-600">Create reusable review boards from the current filtered company set for placement strategy meetings, shortlisting, and batch-level planning.</p>
      </div>

      <ActiveFilterChips filters={filters} onClear={(key) => updateFilter(key, DEFAULT_FILTERS[key])} />

      <section className="grid grid-cols-1 gap-6 rounded-[30px] border border-zinc-200 bg-white/90 p-6 shadow-[0_18px_40px_rgba(15,23,42,0.08)] xl:grid-cols-[0.78fr_1.22fr]" data-testid="review-board-builder">
        <div className="space-y-4">
          <div>
            <label className="mb-2 block text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Board name</label>
            <input className="h-12 w-full rounded-2xl border border-zinc-200 bg-zinc-50 px-4 text-sm text-zinc-900 outline-none focus:border-zinc-900" data-testid="review-board-name-input" onChange={(event) => setName(event.target.value)} placeholder="Top Product Companies 2026" value={name} />
          </div>
          <div>
            <label className="mb-2 block text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Description</label>
            <textarea className="min-h-28 w-full rounded-[22px] border border-zinc-200 bg-zinc-50 px-4 py-3 text-sm text-zinc-900 outline-none focus:border-zinc-900" data-testid="review-board-description-input" onChange={(event) => setDescription(event.target.value)} placeholder="Use this board for shortlisting product-focused, low-risk companies for committee review." value={description} />
          </div>
          <Button className="rounded-full bg-[#0055ff] text-white hover:bg-[#0044cc]" data-testid="review-board-save-button" onClick={saveBoard}>
            <FolderPlus className="mr-2 h-4 w-4" /> Create board
          </Button>
        </div>

        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Add companies from filtered list</p>
            <p className="text-sm text-zinc-600">{selectedCompanyIds.length} selected</p>
          </div>
          <div className="grid max-h-[360px] grid-cols-1 gap-3 overflow-y-auto pr-2">
            {filteredCompanies.map((company) => {
              const checked = selectedCompanyIds.includes(String(company.company_id));
              return (
                <label className={`flex items-start gap-3 rounded-3xl border px-4 py-4 transition ${checked ? "border-zinc-900 bg-zinc-950 text-white" : "border-zinc-200 bg-zinc-50 text-zinc-900"}`} data-testid={`review-board-company-option-${company.company_id}`} key={company.company_id}>
                  <input checked={checked} className="mt-1" onChange={() => toggleCompany(String(company.company_id))} type="checkbox" />
                  <div>
                    <p className="text-sm font-medium">{company["Company Name"]}</p>
                    <p className={`text-xs ${checked ? "text-zinc-300" : "text-zinc-500"}`}>{company.Category} · {company["Hiring Velocity"] || "Hiring signal unavailable"}</p>
                  </div>
                </label>
              );
            })}
          </div>
        </div>
      </section>

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
        {boards.length ? boards.map((board) => {
          const companiesInBoard = board.companyIds.map((id) => companyMap.get(String(id))).filter(Boolean);
          const boardAnalytics = buildAnalyticsFromCompanies(companiesInBoard);
          const riskSignals = companiesInBoard.filter((company) => String(company["Burnout risk"] || "").toLowerCase().includes("high") || company["Legal Issues / Controversies"]);

          return (
            <section className="space-y-5 rounded-[30px] border border-zinc-200 bg-white/90 p-6 shadow-[0_18px_40px_rgba(15,23,42,0.08)]" data-testid={`review-board-card-${board.id}`} key={board.id}>
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Board view</p>
                  <h2 className="mt-2 text-3xl font-medium tracking-tight text-zinc-950">{board.name}</h2>
                  <p className="mt-2 text-sm leading-relaxed text-zinc-600">{board.description || "No description provided."}</p>
                </div>
                <Button className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid={`review-board-delete-${board.id}`} onClick={() => deleteBoard(board.id)} variant="outline">
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>

              <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                <div className="rounded-3xl border border-zinc-200 bg-zinc-50 px-4 py-4" data-testid={`review-board-summary-count-${board.id}`}>
                  <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Companies</p>
                  <p className="mt-2 text-3xl font-medium tracking-tight text-zinc-950">{companiesInBoard.length}</p>
                </div>
                <div className="rounded-3xl border border-zinc-200 bg-zinc-50 px-4 py-4" data-testid={`review-board-summary-hiring-${board.id}`}>
                  <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Hiring signals</p>
                  <p className="mt-2 text-sm text-zinc-700">{(boardAnalytics.hiring_velocity_distribution || []).slice(0, 2).map((item) => `${item.label} (${item.value})`).join(" · ") || "No hiring signal yet"}</p>
                </div>
                <div className="rounded-3xl border border-zinc-200 bg-zinc-50 px-4 py-4" data-testid={`review-board-summary-risks-${board.id}`}>
                  <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Risk indicators</p>
                  <p className="mt-2 text-sm text-zinc-700">{riskSignals.length ? `${riskSignals.length} flagged companies` : "No flagged companies"}</p>
                </div>
              </div>

              <div className="flex flex-wrap gap-3">
                <Button className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid={`review-board-export-csv-${board.id}`} onClick={() => exportFacultyBriefingCsv({ analytics: boardAnalytics, companies: companiesInBoard })} variant="outline">
                  <FileDown className="mr-2 h-4 w-4" /> Export CSV
                </Button>
                <Button className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid={`review-board-export-pdf-${board.id}`} onClick={() => openFacultyPdfReport({ title: board.name, description: board.description, analytics: boardAnalytics, companies: companiesInBoard })} variant="outline">
                  <FileDown className="mr-2 h-4 w-4" /> Export PDF
                </Button>
              </div>

              <div className="space-y-3">
                {companiesInBoard.map((company) => (
                  <div className="rounded-3xl border border-zinc-200 bg-zinc-50 px-4 py-4" data-testid={`review-board-company-${board.id}-${company.company_id}`} key={company.company_id}>
                    <div className="flex flex-col gap-1 lg:flex-row lg:items-center lg:justify-between">
                      <p className="text-sm font-medium text-zinc-950">{company["Company Name"]}</p>
                      <p className="text-xs text-zinc-500">{company.Category} · {company["Employee Size"] || "Employee size unavailable"}</p>
                    </div>
                    <p className="mt-2 text-sm text-zinc-600">Hiring: {company["Hiring Velocity"] || "—"} · Profitability: {company["Profitability Status"] || "—"} · Burnout risk: {company["Burnout risk"] || "—"}</p>
                  </div>
                ))}
              </div>
            </section>
          );
        }) : <PageState description="Create a review board from the current filtered company set to support faculty planning discussions." testId="review-board-empty-state" title="No faculty review boards yet" />}
      </div>
    </div>
  );
};

export default FacultyReviewBoardsPage;