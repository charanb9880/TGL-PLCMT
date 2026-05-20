import { motion } from "framer-motion";
import { ArrowUpRight, Link2 } from "lucide-react";

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Badge } from "@/components/ui/badge";
import { formatValue, isUrl } from "@/lib/formatters";
import { getFieldValue } from "@/lib/fieldMapper";


export default function CompanyFrameSection({ company, section, index }) {
  const sectionValues = section.fields.filter((field) => getFieldValue(company, field) !== null && field !== "Logo");

  return (
    <section
      className="relative flex min-h-screen snap-start items-center overflow-hidden rounded-[36px] border border-zinc-200 bg-white/90 px-6 py-10 shadow-[0_20px_60px_rgba(15,23,42,0.08)] md:px-10 lg:px-12"
      data-testid={`company-frame-${section.id}`}
      id={section.id}
    >
      <div className="pointer-events-none absolute inset-y-0 right-0 hidden w-1/2 overflow-hidden rounded-l-[36px] lg:block">
        <img alt={section.title} className="h-full w-full object-cover object-center opacity-30" src={section.image} />
        <div className="absolute inset-0 bg-gradient-to-l from-white/30 via-white/70 to-white" />
      </div>

      <div className="relative z-10 grid w-full grid-cols-1 gap-10 lg:grid-cols-[0.9fr_1.1fr]">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.03, duration: 0.35 }}
        >
          <Badge className="mb-5 rounded-full border-zinc-300 bg-white/80 px-4 py-2 text-zinc-700" data-testid={`company-frame-badge-${section.id}`} variant="outline">
            <section.icon className="mr-2 h-4 w-4 text-[#0055ff]" /> Frame {index + 1}
          </Badge>
          <h2 className="max-w-xl text-4xl font-medium tracking-tight text-zinc-950 sm:text-5xl" data-testid={`company-frame-title-${section.id}`}>
            {section.title}
          </h2>
          <p className="mt-4 max-w-xl text-base leading-relaxed text-zinc-600" data-testid={`company-frame-description-${section.id}`}>
            Each micro-panel below renders exact schema fields without renaming or combining columns.
          </p>

          <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2">
            {sectionValues.slice(0, 4).map((field) => (
              <div className="rounded-3xl border border-zinc-200 bg-zinc-50/90 px-5 py-4" data-testid={`company-frame-highlight-${section.id}-${field.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`} key={field}>
                <p className="mb-2 text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">{field}</p>
                <p className="text-sm leading-relaxed text-zinc-800">{formatValue(getFieldValue(company, field))}</p>
              </div>
            ))}
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.04, duration: 0.35 }}
        >
          <Accordion className="rounded-[28px] border border-zinc-200 bg-white/80 px-6" collapsible type="single">
            {sectionValues.map((field) => (
              <AccordionItem key={field} value={field}>
                <AccordionTrigger className="py-5 text-left text-sm font-medium text-zinc-900" data-testid={`company-frame-accordion-trigger-${section.id}-${field.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}>
                  <span className="flex items-center gap-3">
                    <span className="inline-flex h-9 w-9 items-center justify-center rounded-full border border-zinc-200 bg-zinc-50 text-zinc-500">
                      <ArrowUpRight className="h-4 w-4" />
                    </span>
                    {field}
                  </span>
                </AccordionTrigger>
                <AccordionContent className="pr-4 text-sm leading-relaxed text-zinc-600" data-testid={`company-frame-accordion-content-${section.id}-${field.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}>
                  {isUrl(getFieldValue(company, field)) ? (
                    field === "Logo" ? (
                      <div className="mt-2 flex h-24 w-24 items-center justify-center rounded-2xl border border-zinc-100 bg-white p-3 shadow-sm">
                        <img alt="Company Logo" className="h-full w-full object-contain" src={getFieldValue(company, field)} />
                      </div>
                    ) : (
                      <a
                        className="inline-flex items-center gap-2 text-[#0055ff] underline-offset-4 hover:underline"
                        data-testid={`company-frame-link-${section.id}-${field.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}
                        href={getFieldValue(company, field)}
                        rel="noreferrer"
                        target="_blank"
                      >
                        <Link2 className="h-4 w-4" />
                        {getFieldValue(company, field)}
                      </a>
                    )
                  ) : (
                    <p>{formatValue(getFieldValue(company, field))}</p>
                  )}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </motion.div>
      </div>
    </section>
  );
}