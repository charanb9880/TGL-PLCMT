import { Suspense, lazy } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import AppShell from "@/components/AppShell";
import PageState from "@/components/PageState";
import { FilterProvider } from "@/context/FilterContext";


const HomePage = lazy(() => import("@/pages/HomePage"));
const ExplorePage = lazy(() => import("@/pages/ExplorePage"));
const CategoriesPage = lazy(() => import("@/pages/CategoriesPage"));
const ComparePage = lazy(() => import("@/pages/ComparePage"));
const SkillMappingPage = lazy(() => import("@/pages/SkillMappingPage"));
const AnalyticsPage = lazy(() => import("@/pages/AnalyticsPage"));
const CompanyDetailPage = lazy(() => import("@/pages/CompanyDetailPage"));
const FacultyReviewBoardsPage = lazy(() => import("@/pages/FacultyReviewBoardsPage"));
const ResearchPage = lazy(() => import("@/pages/ResearchPage"));

function App() {
  return (
    <BrowserRouter>
      <FilterProvider>
        <AppShell>
          <Suspense fallback={<PageState description="Loading the next experience." loading testId="route-loading-state" title="Opening page" />}>
            <Routes>
              <Route element={<HomePage />} path="/" />
              <Route element={<ExplorePage />} path="/explore" />
              <Route element={<CategoriesPage />} path="/categories" />
              <Route element={<ComparePage />} path="/compare" />
              <Route element={<SkillMappingPage />} path="/skill-mapping" />
              <Route element={<AnalyticsPage />} path="/analytics" />
              <Route element={<FacultyReviewBoardsPage />} path="/faculty/review-boards" />
              <Route element={<CompanyDetailPage />} path="/company/:companyId" />
              <Route element={<ResearchPage />} path="/research" />
            </Routes>
          </Suspense>
        </AppShell>
      </FilterProvider>
    </BrowserRouter>
  );
}

export default App;
