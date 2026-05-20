import { motion } from "framer-motion";
import { Compass, DatabaseZap } from "lucide-react";
import { NavLink } from "react-router-dom";

import InstallPromptBanner from "@/components/InstallPromptBanner";
import { NAV_ITEMS } from "@/lib/companyFrames";
import usePlacementFilters from "@/hooks/usePlacementFilters";


const linkClasses = ({ isActive }) =>
  `whitespace-nowrap rounded-full border px-3 py-2 text-[13px] transition-colors ${
    isActive
      ? "border-zinc-900 bg-zinc-950 text-white"
      : "border-zinc-200 bg-white/70 text-zinc-600 hover:border-zinc-900 hover:text-zinc-950"
  }`;


export default function AppShell({ children }) {
  const { buildRouteTarget } = usePlacementFilters();

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,#ffffff_0%,#f7f7f5_40%,#eff3f7_100%)] text-zinc-950">
      <motion.header
        className="sticky top-0 z-50 border-b border-white/60 bg-white/75 backdrop-blur-xl"
        initial={{ opacity: 0, y: -24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <div className="mx-auto max-w-7xl px-6 py-5 lg:px-10 xl:grid xl:grid-cols-[220px_minmax(0,1fr)_280px] xl:items-center xl:gap-6">
          <div className="flex items-center gap-3" data-testid="global-brand-lockup">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-zinc-200 bg-white shadow-sm">
              <Compass className="h-5 w-5 text-[#0055ff]" />
            </div>
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.35em] text-zinc-500">PES</p>
              <h1 className="text-lg font-medium tracking-tight text-zinc-950">Placement Intelligence</h1>
            </div>
          </div>

          <nav className="flex flex-nowrap gap-2 overflow-x-auto" data-testid="global-navigation">
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.path}
                className={linkClasses}
                data-testid={`nav-link-${item.label.toLowerCase().replace(/\s+/g, "-")}`}
                end={item.path === "/"}
                to={buildRouteTarget(item.path)}
              >
                {item.label}
              </NavLink>
            ))}
          </nav>

          <div
            className="mt-4 hidden items-center justify-end gap-2 rounded-full border border-zinc-200 bg-white px-4 py-2 text-sm text-zinc-600 xl:mt-0 xl:inline-flex"
            data-testid="dataset-mode-indicator"
          >
            <DatabaseZap className="h-4 w-4 text-[#0055ff]" />
            Schema-driven placement intelligence
          </div>
        </div>
      </motion.header>

      <main className="mx-auto max-w-7xl px-6 pb-16 pt-8 lg:px-10">
        <InstallPromptBanner />
        {children}
      </main>
    </div>
  );
}