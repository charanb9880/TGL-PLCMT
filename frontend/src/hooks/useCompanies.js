import { useEffect, useMemo, useState } from "react";

import useDebouncedValue from "@/hooks/useDebouncedValue";
import { fetchCompanies as apiFetchCompanies } from "@/lib/api";
import { getFieldValue } from "@/lib/fieldMapper";


const COMPANY_CACHE_KEY = "public-company-cache";
const memoryCache = new Map();


const normalizeValue = (value) => String(value || "").trim().toLowerCase();


const sortValue = (value) => {
  const text = String(value ?? "").trim().toLowerCase();
  const match = text.match(/-?\d[\d,.]*/);
  if (match) {
    return Number(match[0].replaceAll(",", ""));
  }
  return text;
};


const applyFilters = (companies, filters) => {
  const search = normalizeValue(filters.search);

  const filtered = companies.filter((company) => {
    if (search) {
      const haystack = [
        getFieldValue(company, "Company Name"),
        getFieldValue(company, "Short Name"),
        getFieldValue(company, "Category"),
        getFieldValue(company, "Focus Sectors / Industries"),
        getFieldValue(company, "Services / Offerings / Products"),
        getFieldValue(company, "Tech Stack/Tools Used"),
      ]
        .map(normalizeValue)
        .join(" ");

      if (!haystack.includes(search)) {
        return false;
      }
    }

    const filterMap = {
      category: "Category",
      focus_sectors: "Focus Sectors / Industries",
      employee_size: "Employee Size",
      profitability_status: "Profitability Status",
      remote_policy_details: "Remote Work Policy",
      hiring_velocity: "Hiring Velocity",
      tech_stack: "Tech Stack/Tools Used",
    };

    return Object.entries(filterMap).every(([filterKey, column]) => {
      const filterValue = normalizeValue(filters[filterKey]);
      return !filterValue || normalizeValue(getFieldValue(company, column)).includes(filterValue);
    });
  });

  const sortMap = {
    name: "Company Name",
    employee_size: "Employee Size",
    yoy_growth_rate: "Year-over-Year Growth Rate",
    brand_value: "Brand value",
  };

  return [...filtered].sort((left, right) => {
    const leftValue = sortValue(getFieldValue(left, sortMap[filters.sort_by] || "Company Name"));
    const rightValue = sortValue(getFieldValue(right, sortMap[filters.sort_by] || "Company Name"));
    if (leftValue < rightValue) {
      return -1;
    }
    if (leftValue > rightValue) {
      return 1;
    }
    return 0;
  });
};


const useCompanies = ({ filters = {}, page = 1, pageSize = 24 } = {}) => {
  const [companies, setCompanies] = useState(memoryCache.get(COMPANY_CACHE_KEY) || []);
  const [loading, setLoading] = useState(!memoryCache.has(COMPANY_CACHE_KEY));
  const [error, setError] = useState("");
  const debouncedSearch = useDebouncedValue(filters.search || "", 250);

  useEffect(() => {
    if (memoryCache.has(COMPANY_CACHE_KEY)) {
      return;
    }

    const loadCompanies = async () => {
      setLoading(true);
      setError("");
      try {
        const response = await apiFetchCompanies({ pageSize: 1000 });
        const data = response.items || [];
        memoryCache.set(COMPANY_CACHE_KEY, data);
        setCompanies(data);
      } catch (err) {
        setError(err.message || "Unable to load companies from backend.");
      } finally {
        setLoading(false);
      }
    };

    loadCompanies();
  }, []);

  const effectiveFilters = useMemo(() => ({ ...filters, search: debouncedSearch }), [debouncedSearch, filters]);
  const filteredCompanies = useMemo(() => applyFilters(companies, effectiveFilters), [companies, effectiveFilters]);
  const paginatedCompanies = useMemo(() => filteredCompanies.slice((page - 1) * pageSize, page * pageSize), [filteredCompanies, page, pageSize]);

  return {
    companies: paginatedCompanies,
    allCompanies: filteredCompanies,
    sourceCompanies: companies,
    total: filteredCompanies.length,
    loading,
    error,
    refresh: () => memoryCache.delete(COMPANY_CACHE_KEY),
  };
};

export default useCompanies;