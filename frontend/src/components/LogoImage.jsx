import { useState } from "react";
import { extractDomain, getLogoUrl } from "@/lib/formatters";
import { getFieldValue } from "@/lib/fieldMapper";

export default function LogoImage({ company, className, fallbackInitials }) {
  const [stage, setStage] = useState(0); // 0: Primary, 1: DDG, 2: Clearbit, 3: Google, 4: Failed
  
  const companyName = getFieldValue(company, "Company Name");
  const website = getFieldValue(company, "Website URL");
  const domain = extractDomain(website);
  const cleanName = String(companyName || "").replace(/(corp|inc|ltd|plc|limited|co)\.?$/i, "").trim().split(/[,\s]/)[0].replace(/[^a-z0-9]/g, "").toLowerCase();
  const targetDomain = domain || `${cleanName}.com`;

  const sources = [
    getLogoUrl(getFieldValue(company, "Logo")),
    `https://icons.duckduckgo.com/ip3/${targetDomain}.ico`,
    `https://logo.clearbit.com/${targetDomain}`,
    `https://www.google.com/s2/favicons?sz=128&domain=${targetDomain}`
  ];

  const currentSrc = sources[stage];

  if (stage >= sources.length || !currentSrc) {
    return fallbackInitials;
  }

  return (
    <img
      alt={companyName}
      className={className}
      src={currentSrc}
      onError={() => setStage((prev) => prev + 1)}
    />
  );
}
