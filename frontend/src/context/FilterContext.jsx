import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";


const STORAGE_KEY = "placement-intelligence-filters-v2";
const SYNC_ROUTES = ["/explore", "/categories", "/analytics"];

export const DEFAULT_FILTERS = {
  search: "",
  category: "",
  focus_sectors: "",
  employee_size: "",
  profitability_status: "",
  remote_policy_details: "",
  hiring_velocity: "",
  sort_by: "name",
};

const FilterContext = createContext(null);


const parseSearchToFilters = (search) => {
  const params = new URLSearchParams(search);
  return {
    search: params.get("search") || "",
    category: params.get("category") || "",
    focus_sectors: params.get("focus_sectors") || "",
    employee_size: params.get("employee_size") || "",
    profitability_status: params.get("profitability_status") || "",
    remote_policy_details: params.get("remote_policy_details") || "",
    hiring_velocity: params.get("hiring_velocity") || "",
    sort_by: params.get("sort_by") || DEFAULT_FILTERS.sort_by,
  };
};


const buildSearchFromFilters = (filters) => {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value && value !== DEFAULT_FILTERS[key]) {
      params.set(key, value);
    }
  });
  return params.toString();
};


const shallowEqual = (left, right) =>
  Object.keys(DEFAULT_FILTERS).every((key) => (left?.[key] || "") === (right?.[key] || ""));


export function FilterProvider({ children }) {
  const location = useLocation();
  const navigate = useNavigate();

  const [filters, setFilters] = useState(() => {
    try {
      const stored = JSON.parse(window.localStorage.getItem(STORAGE_KEY) || "{}");
      return { ...DEFAULT_FILTERS, ...stored, ...parseSearchToFilters(window.location.search) };
    } catch {
      return DEFAULT_FILTERS;
    }
  });

  const isSyncRoute = SYNC_ROUTES.includes(location.pathname);

  useEffect(() => {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(filters));
  }, [filters]);

  useEffect(() => {
    if (!isSyncRoute) {
      return;
    }

    const queryFilters = parseSearchToFilters(location.search);
    setFilters((previous) => {
      const next = { ...DEFAULT_FILTERS, ...previous, ...queryFilters };
      return shallowEqual(previous, next) ? previous : next;
    });
  }, [isSyncRoute, location.search]);

  useEffect(() => {
    if (!isSyncRoute) {
      return;
    }

    const nextSearch = buildSearchFromFilters(filters);
    const currentSearch = location.search.replace(/^\?/, "");

    if (nextSearch !== currentSearch) {
      navigate({ pathname: location.pathname, search: nextSearch ? `?${nextSearch}` : "" }, { replace: true });
    }
  }, [filters, isSyncRoute, location.pathname, location.search, navigate]);

  const updateFilter = (key, value) => {
    setFilters((previous) => ({ ...previous, [key]: value }));
  };

  const updateManyFilters = (nextValues) => {
    setFilters((previous) => ({ ...previous, ...nextValues }));
  };

  const resetFilters = () => {
    setFilters(DEFAULT_FILTERS);
  };

  const buildRouteTarget = (path, overrides = {}) => {
    if (!SYNC_ROUTES.includes(path)) {
      return path;
    }
    const nextSearch = buildSearchFromFilters({ ...filters, ...overrides });
    return nextSearch ? `${path}?${nextSearch}` : path;
  };

  const value = useMemo(
    () => ({
      filters,
      updateFilter,
      updateManyFilters,
      resetFilters,
      buildRouteTarget,
      activeFilterCount: Object.entries(filters).filter(([key, value]) => key !== "sort_by" && value).length,
    }),
    [filters],
  );

  return <FilterContext.Provider value={value}>{children}</FilterContext.Provider>;
}


export const useFilterContext = () => {
  const context = useContext(FilterContext);
  if (!context) {
    throw new Error("useFilterContext must be used inside FilterProvider");
  }
  return context;
};