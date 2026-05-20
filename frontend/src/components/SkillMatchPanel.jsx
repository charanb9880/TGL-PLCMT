import { useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";


export default function SkillMatchPanel({ companies = [], onRun, result, loading }) {
  const [companyId, setCompanyId] = useState("");
  const [skills, setSkills] = useState("");

  const disabled = useMemo(() => !companyId || !skills.trim() || loading, [companyId, skills, loading]);

  return (
    <section className="grid grid-cols-1 gap-6 xl:grid-cols-[0.78fr_1.22fr]" data-testid="skill-match-panel">
      <div className="rounded-[28px] border border-zinc-200 bg-white/90 p-6 shadow-[0_18px_50px_rgba(15,23,42,0.08)]">
        <p className="text-xs font-bold uppercase tracking-[0.28em] text-zinc-500">Rule-based input</p>
        <h2 className="mt-2 text-3xl font-medium tracking-tight text-zinc-950">Map your skills to company expectations</h2>
        <p className="mt-3 text-sm leading-relaxed text-zinc-600">
          This workflow checks your skills against exact company fields like Tech Stack/Tools Used, AI/ML Adoption Level, Automation level, and Skill relevance.
        </p>

        <div className="mt-8 space-y-5">
          <div>
            <label className="mb-2 block text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Company</label>
            <Select onValueChange={setCompanyId} value={companyId}>
              <SelectTrigger className="h-12 rounded-2xl border-zinc-200 bg-zinc-50" data-testid="skill-match-company-select">
                <SelectValue placeholder="Select a company" />
              </SelectTrigger>
              <SelectContent>
                {companies.map((company) => (
                  <SelectItem key={company.company_id} value={String(company.company_id)}>
                    {company["Company Name"]}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div>
            <label className="mb-2 block text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Your skills</label>
            <textarea
              className="min-h-48 w-full rounded-[24px] border border-zinc-200 bg-zinc-50 px-4 py-4 text-sm text-zinc-800 outline-none transition focus:border-zinc-900"
              data-testid="skill-match-skills-input"
              onChange={(event) => setSkills(event.target.value)}
              placeholder="Example: Python, React, SQL, ML evaluation, system design"
              value={skills}
            />
          </div>

          <Button className="w-full rounded-full bg-[#0055ff] py-6 text-white hover:bg-[#0044cc]" data-testid="skill-match-run-button" disabled={disabled} onClick={() => onRun({ company_id: companyId, skills })}>
            {loading ? "Running skill match..." : "Run rule-based skill mapping"}
          </Button>
        </div>
      </div>

      <div className="rounded-[28px] border border-zinc-200 bg-white/90 p-6 shadow-[0_18px_50px_rgba(15,23,42,0.08)]" data-testid="skill-match-results">
        <p className="text-xs font-bold uppercase tracking-[0.28em] text-zinc-500">Skill fit output</p>
        <h3 className="mt-2 text-3xl font-medium tracking-tight text-zinc-950">Preparation signals</h3>

        {result ? (
          <div className="mt-8 space-y-6">
            <div className="rounded-3xl border border-zinc-200 bg-zinc-50 px-5 py-4" data-testid="skill-match-fit-level">
              <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Fit level</p>
              <p className="mt-2 text-4xl font-medium tracking-tight text-zinc-950">{result.result.fit_level}</p>
              <p className="mt-2 text-sm text-zinc-600">Match score: {result.result.match_score}/100</p>
            </div>

            <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
              <div className="rounded-3xl border border-zinc-200 bg-zinc-50 p-5" data-testid="skill-match-matched-skills">
                <p className="mb-3 text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Matched skills</p>
                <ul className="space-y-2 text-sm text-zinc-700">
                  {(result.result.matched_skills || []).length ? result.result.matched_skills.map((item) => <li key={item}>• {item}</li>) : <li>• No direct matches yet</li>}
                </ul>
              </div>

              <div className="rounded-3xl border border-zinc-200 bg-zinc-50 p-5" data-testid="skill-match-skill-gaps">
                <p className="mb-3 text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Skill gaps</p>
                <ul className="space-y-2 text-sm text-zinc-700">
                  {(result.result.skill_gaps || []).length ? result.result.skill_gaps.map((item) => <li key={item}>• {item}</li>) : <li>• No major gaps detected</li>}
                </ul>
              </div>
            </div>

            <div className="rounded-3xl border border-zinc-200 bg-zinc-50 p-5" data-testid="skill-match-preparation-suggestions">
              <p className="mb-3 text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Preparation suggestions</p>
              <ul className="space-y-2 text-sm text-zinc-700">
                {(result.result.preparation_suggestions || []).map((item) => <li key={item}>• {item}</li>)}
              </ul>
            </div>
          </div>
        ) : (
          <div className="mt-8 rounded-[28px] border border-dashed border-zinc-300 bg-zinc-50/70 px-6 py-12 text-center text-sm leading-relaxed text-zinc-600" data-testid="skill-match-empty-state">
            Pick a company and enter your skills to generate high / medium / low fit, gaps, and preparation suggestions.
          </div>
        )}
      </div>
    </section>
  );
}