import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { COMPARISON_SECTIONS } from "@/lib/companyFrames";
import { formatValue } from "@/lib/formatters";


const HighlightList = ({ title, items, testId }) => (
  <div className="rounded-3xl border border-zinc-200 bg-zinc-50 p-5" data-testid={testId}>
    <p className="mb-3 text-xs font-bold uppercase tracking-[0.28em] text-zinc-500">{title}</p>
    <ul className="space-y-2 text-sm text-zinc-700">
      {(items || []).length ? (items || []).map((item) => <li key={item}>• {item}</li>) : <li>• No rule-based highlight yet</li>}
    </ul>
  </div>
);


export default function ComparisonTable({ comparison }) {
  if (!comparison) {
    return null;
  }

  const { left_company: leftCompany, right_company: rightCompany, left_highlights: leftHighlights, right_highlights: rightHighlights } = comparison;

  return (
    <section className="space-y-8" data-testid="comparison-results-section">
      <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
        <HighlightList items={leftHighlights?.strengths} testId="comparison-left-strengths" title={`${leftCompany?.["Short Name"] || leftCompany?.["Company Name"]} strengths`} />
        <HighlightList items={rightHighlights?.strengths} testId="comparison-right-strengths" title={`${rightCompany?.["Short Name"] || rightCompany?.["Company Name"]} strengths`} />
        <HighlightList items={leftHighlights?.risks} testId="comparison-left-risks" title={`${leftCompany?.["Short Name"] || leftCompany?.["Company Name"]} risks`} />
        <HighlightList items={rightHighlights?.risks} testId="comparison-right-risks" title={`${rightCompany?.["Short Name"] || rightCompany?.["Company Name"]} risks`} />
      </div>

      {COMPARISON_SECTIONS.map((section) => (
        <div className="rounded-[28px] border border-zinc-200 bg-white/90 p-6 shadow-[0_18px_50px_rgba(15,23,42,0.08)]" data-testid={`comparison-table-${section.title.toLowerCase()}`} key={section.title}>
          <div className="mb-5">
            <p className="text-xs font-bold uppercase tracking-[0.28em] text-zinc-500">Section</p>
            <h3 className="text-2xl font-medium tracking-tight text-zinc-950">{section.title}</h3>
          </div>

          <Table>
            <TableHeader>
              <TableRow>
                <TableHead data-testid={`comparison-heading-field-${section.title.toLowerCase()}`}>Exact field</TableHead>
                <TableHead data-testid={`comparison-heading-left-${section.title.toLowerCase()}`}>{leftCompany?.["Short Name"] || leftCompany?.["Company Name"]}</TableHead>
                <TableHead data-testid={`comparison-heading-right-${section.title.toLowerCase()}`}>{rightCompany?.["Short Name"] || rightCompany?.["Company Name"]}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {section.fields.map((field) => (
                <TableRow key={`${section.title}-${field}`}>
                  <TableCell data-testid={`comparison-field-${field.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}>{field}</TableCell>
                  <TableCell data-testid={`comparison-left-value-${field.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}>{formatValue(leftCompany?.[field])}</TableCell>
                  <TableCell data-testid={`comparison-right-value-${field.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}>{formatValue(rightCompany?.[field])}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      ))}
    </section>
  );
}