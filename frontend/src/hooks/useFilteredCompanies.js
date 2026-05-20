import useCompanies from "@/hooks/useCompanies";


const useFilteredCompanies = (filters, options = {}) => {
  return useCompanies({ filters, ...options });
}

export default useFilteredCompanies;
