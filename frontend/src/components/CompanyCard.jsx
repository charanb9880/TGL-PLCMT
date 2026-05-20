import { motion } from "framer-motion";
import { ArrowUpRight, Building2, MapPin, Users } from "lucide-react";
import { Link } from "react-router-dom";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { VISUALS } from "@/lib/companyFrames";
import { getCompanyIdentifier, truncate } from "@/lib/formatters";
import { getFieldValue } from "@/lib/fieldMapper";
import LogoImage from "./LogoImage";


const getInitials = (name) => {
  if (!name || typeof name !== "string") return "CO";
  return name
    .split(" ")
    .map((part) => (part[0] ? part[0] : ""))
    .join("")
    .slice(0, 2)
    .toUpperCase();
};

const pickContextualVisual = (company) => {
  const category = String(getFieldValue(company, "Category") || "").toLowerCase();
  const sector = String(getFieldValue(company, "Focus Sectors / Industries") || "").toLowerCase();

  if (category.includes("fintech") || sector.includes("ai") || sector.includes("cloud") || sector.includes("data")) {
    return VISUALS.technology;
  }
  if (category.includes("service") || category.includes("consulting")) {
    return VISUALS.office;
  }
  return VISUALS.data;
};


export default function CompanyCard({ company }) {
  const identifier = getCompanyIdentifier(company);
  const heroVisual = pickContextualVisual(company);
  const companyName = getFieldValue(company, "Company Name") || "Untitled Entity";
  const companyInitials = getInitials(companyName);

  return (
    <motion.div whileHover={{ y: -4 }} transition={{ duration: 0.18 }}>
      <Card className="overflow-hidden rounded-[28px] border-zinc-200 bg-white/90 shadow-[0_12px_40px_rgba(15,23,42,0.08)]" data-testid={`company-card-${identifier}`}>
        <div className="relative h-64 w-full overflow-hidden border-b border-zinc-100 bg-white lg:h-72">
          <LogoImage 
            company={company}
            className="h-full w-full object-contain p-10 object-center transition-opacity duration-300"
            fallbackInitials={
                <img 
                    alt="fallback" 
                    className="h-full w-full object-cover object-center bg-gradient-to-br from-zinc-100 via-white to-zinc-200" 
                    src={heroVisual} 
                />
            }
          />

          <div className="absolute left-5 top-5">
            <Badge className="border border-white/60 bg-white/85 text-zinc-900" data-testid={`company-card-category-${identifier}`} variant="outline">
              {getFieldValue(company, "Category") || "Category unavailable"}
            </Badge>
          </div>

          <div className="absolute right-5 top-5 flex h-12 w-12 items-center justify-center overflow-hidden rounded-2xl border border-white/70 bg-white/85 shadow-sm" data-testid={`company-card-logo-badge-${identifier}`}>
            <LogoImage 
                company={company}
                className="h-full w-full object-contain p-2"
                fallbackInitials={
                    <span className="text-sm font-bold text-zinc-900">
                        {companyInitials || <Building2 className="h-5 w-5 text-zinc-500" />}
                    </span>
                }
            />
          </div>
        </div>

        <CardContent className="space-y-5 p-6">
          <div className="space-y-2">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.3em] text-zinc-500" data-testid={`company-card-short-name-${identifier}`}>
                  {getFieldValue(company, "Short Name") || "Short name unavailable"}
                </p>
                <h3 className="text-3xl font-medium tracking-tight text-zinc-950" data-testid={`company-card-name-${identifier}`}>
                  {companyName || "Untitled Entity"}
                </h3>
              </div>
              {company.company_id && (
                <Link to={`/company/${identifier}`}>
                  <Button className="h-12 w-12 rounded-full bg-zinc-50 p-0 text-zinc-400 hover:bg-zinc-900 hover:text-white" data-testid={`company-card-link-${identifier}`} variant="ghost">
                    <ArrowUpRight className="h-5 w-5" />
                  </Button>
                </Link>
              )}
            </div>

            <p className="text-sm leading-relaxed text-zinc-600" data-testid={`company-card-overview-${identifier}`}>
              {truncate(getFieldValue(company, "Overview of the Company"), 140)}
            </p>
          </div>

          <div className="flex flex-wrap gap-2 pt-2">
            <div className="mr-4 flex items-center gap-1.5 text-zinc-500">
              <MapPin className="h-4 w-4" />
              <span className="text-xs font-medium">{getFieldValue(company, "Company Headquarters") || "Global"}</span>
            </div>
            <div className="flex items-center gap-1.5 text-zinc-500">
              <Users className="h-4 w-4" />
              <span className="text-xs font-medium">{getFieldValue(company, "Employee Size") || "Confidential"}</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}