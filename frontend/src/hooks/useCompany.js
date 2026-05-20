import { useEffect, useState } from "react";

import { fetchCompany } from "@/lib/api";

const useCompany = (companyId) => {
  const [company, setCompany] = useState(null);
  const [highlights, setHighlights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!companyId) {
      setLoading(false);
      setCompany(null);
      setHighlights(null);
      return;
    }

    const loadCompany = async () => {
      setLoading(true);
      setError("");
      
      try {
        const data = await fetchCompany(companyId);
        setCompany(data.company);
        setHighlights(data.highlights);
      } catch (err) {
        setError(err.message || "Unable to load company from backend.");
      } finally {
        setLoading(false);
      }
    };

    loadCompany();
  }, [companyId]);

  return { company, highlights, loading, error };
}

export default useCompany;

