import { useEffect, useState } from "react";
import { ArrowRight, Dot } from "lucide-react";
import { useParams } from "react-router-dom";

import CompanyFrameSection from "@/components/CompanyFrameSection";
import DataSkeleton from "@/components/DataSkeleton";
import PageState from "@/components/PageState";
import { Button } from "@/components/ui/button";
import useCompany from "@/hooks/useCompany";
import { COMPANY_FRAME_SECTIONS } from "@/lib/companyFrames";
import { buildCompanyHighlights } from "@/lib/highlights";
import { getFieldValue } from "@/lib/fieldMapper";
import LogoImage from "@/components/LogoImage";


const CompanyDetailPage = () => {
  const { companyId } = useParams();
  const { company, loading, error } = useCompany(companyId);
  const [activeSectionId, setActiveSectionId] = useState(COMPANY_FRAME_SECTIONS[0].id);
  const [scrollProgress, setScrollProgress] = useState(0);
  const highlights = buildCompanyHighlights(company || {});

  const getRelativeTop = (container, element) => {
    const containerBox = container.getBoundingClientRect();
    const elementBox = element.getBoundingClientRect();
    return elementBox.top - containerBox.top + container.scrollTop;
  };

  const scrollToSection = (sectionId) => {
    const container = document.querySelector('[data-testid="company-detail-frame-container"]');
    const section = document.getElementById(sectionId);
    if (container && section) {
      container.scrollTo({ top: getRelativeTop(container, section), behavior: "smooth" });
    }
  };

  useEffect(() => {
    const container = document.querySelector('[data-testid="company-detail-frame-container"]');
    if (!container || !company) {
      return undefined;
    }

    const syncScrollState = () => {
      const maxScroll = container.scrollHeight - container.clientHeight;
      const progress = maxScroll <= 0 ? 0 : (container.scrollTop / maxScroll) * 100;
      setScrollProgress(Math.min(100, Math.max(0, progress)));

      const threshold = container.scrollTop + container.clientHeight * 0.35;
      let currentSection = COMPANY_FRAME_SECTIONS[0].id;
      COMPANY_FRAME_SECTIONS.forEach((section) => {
        const element = document.getElementById(section.id);
        if (element) {
          const relativeTop = getRelativeTop(container, element);
          if (relativeTop <= threshold) {
            currentSection = section.id;
          }
        }
      });
      setActiveSectionId(currentSection);
    };

    container.addEventListener("scroll", syncScrollState);
    return () => container.removeEventListener("scroll", syncScrollState);
  }, [company]);

  if (loading) return <DataSkeleton />;
  if (error) return <PageState error={error} title="Data pipeline error" />;
  if (!company) return <PageState title="Company intelligence not found" />;

  return (
    <div className="relative flex h-screen flex-col overflow-hidden bg-zinc-50" data-testid={`company-detail-page-${companyId}`}>
      {/* Header Overlay */}
      <header className="z-30 border-b border-zinc-200 bg-white/80 px-8 py-10 shadow-sm backdrop-blur-md lg:px-12">
        <div className="flex flex-col items-start justify-between gap-6 md:flex-row md:items-center">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.3em] text-zinc-500">Company detail</p>
            <div className="mt-2 flex items-center gap-6">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl border border-zinc-200 bg-white p-2 shadow-sm overflow-hidden">
                <LogoImage 
                    company={company}
                    className="h-full w-full object-contain"
                    fallbackInitials={null}
                />
              </div>
              <h1 className="text-5xl font-medium tracking-tight text-zinc-950" data-testid="company-detail-title">
                {getFieldValue(company, "Company Name") || "Loading company..."}
              </h1>
            </div>
            <p className="mt-4 max-w-3xl text-base leading-relaxed text-zinc-600" data-testid="company-detail-overview-text">
              {getFieldValue(company, "Overview of the Company") || "The full 10-frame experience below renders company detail using exact schema fields."}
            </p>
          </div>

          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <div className="rounded-3xl border border-zinc-200 bg-zinc-50 px-4 py-4" data-testid="company-detail-highlight-strengths">
              <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Strengths</p>
              <ul className="mt-3 space-y-2 text-sm text-zinc-700">
                {(highlights?.strengths || []).map((item) => <li key={item}>• {item}</li>)}
              </ul>
            </div>
            <div className="rounded-3xl border border-zinc-200 bg-zinc-50 px-4 py-4" data-testid="company-detail-highlight-weaknesses">
              <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Benchmark</p>
              <ul className="mt-3 space-y-2 text-sm text-zinc-700">
                {(highlights?.weaknesses || []).map((item) => <li key={item}>• {item}</li>)}
              </ul>
            </div>
            <div className="rounded-3xl border border-zinc-200 bg-zinc-50 px-4 py-4" data-testid="company-detail-highlight-risks">
              <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Risk Profile</p>
              <ul className="mt-3 space-y-2 text-sm text-zinc-700">
                {(highlights?.risks || []).map((item) => <li key={item}>• {item}</li>)}
              </ul>
            </div>
          </div>
        </div>
      </header>

      <div className="relative flex flex-1 overflow-hidden">
        {/* Navigation Sidebar */}
        <aside className="hidden w-28 flex-col items-center border-r border-zinc-200 bg-white/50 py-8 lg:flex">
          <div className="sticky top-28 flex h-fit flex-col items-center gap-4 rounded-[28px] border border-zinc-200 bg-white/85 px-3 py-5 shadow-[0_18px_40px_rgba(15,23,42,0.08)]" data-testid="company-detail-sidebar">
            <div className="w-full rounded-[22px] border border-zinc-200 bg-zinc-50 px-3 py-4 text-center" data-testid="company-detail-progress-card">
              <p className="text-[10px] font-bold uppercase tracking-[0.28em] text-zinc-500">Progress</p>
              <p className="mt-2 text-2xl font-medium tracking-tight text-zinc-950">{Math.round(scrollProgress)}%</p>
              <div className="mx-auto mt-3 flex h-28 w-2 items-end rounded-full bg-zinc-200" data-testid="company-detail-progress-track">
                <div className="w-full rounded-full bg-[#0055ff] transition-all" data-testid="company-detail-progress-fill" style={{ height: `${Math.max(scrollProgress, 8)}%` }} />
              </div>
              <p className="mt-3 text-xs text-zinc-600">{COMPANY_FRAME_SECTIONS.find((section) => section.id === activeSectionId)?.title}</p>
            </div>

            {COMPANY_FRAME_SECTIONS.map((section) => (
              <button
                className={`flex h-11 w-11 items-center justify-center rounded-full border transition ${activeSectionId === section.id ? "border-zinc-900 bg-zinc-950 text-white" : "border-zinc-200 bg-zinc-50 text-zinc-500 hover:border-zinc-900 hover:text-zinc-950"}`}
                data-testid={`company-detail-nav-${section.id}`}
                key={section.id}
                onClick={() => scrollToSection(section.id)}
                type="button"
              >
                <section.icon className="h-4 w-4" />
              </button>
            ))}
          </div>
        </aside>

        {/* Dynamic Snap Frames */}
        <main
          className="flex-1 snap-y snap-mandatory overflow-y-auto scroll-smooth pb-20 pt-8"
          data-testid="company-detail-frame-container"
        >
          <div className="mx-auto max-w-7xl space-y-12 px-8 lg:px-12">
            {COMPANY_FRAME_SECTIONS.map((section, idx) => (
              <CompanyFrameSection
                company={company}
                index={idx}
                key={section.id}
                section={section}
              />
            ))}
          </div>
        </main>
      </div>

      {/* Quick Action FAB */}
      <div className="fixed bottom-10 right-10 z-40">
        <Button
          className="h-16 rounded-full bg-zinc-950 px-8 text-white shadow-2xl hover:bg-zinc-900"
          data-testid="company-detail-fab"
          onClick={() => window.open(getFieldValue(company, "Website URL"), "_blank")}
        >
          Explore Website <ArrowRight className="ml-3 h-5 w-5" />
        </Button>
      </div>
    </div>
  );
}

export default CompanyDetailPage;
