import { useEffect, useState } from "react";
import { BookmarkPlus, Copy, FolderOpen, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/button";


const STORAGE_KEY = "placement-saved-dashboards-v1";


export default function SavedDashboards({ buildDashboardUrl, filters, onApplyDashboard }) {
  const [dashboards, setDashboards] = useState([]);
  const [name, setName] = useState("");

  useEffect(() => {
    setDashboards(JSON.parse(window.localStorage.getItem(STORAGE_KEY) || "[]"));
  }, []);

  const saveDashboard = () => {
    if (!name.trim()) {
      return;
    }
    const dashboardId = Date.now();
    const nextDashboards = [
      { id: dashboardId, name: name.trim(), filters, url: buildDashboardUrl(filters, dashboardId) },
      ...dashboards,
    ];
    setDashboards(nextDashboards);
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(nextDashboards));
    setName("");
  };

  const deleteDashboard = (id) => {
    const nextDashboards = dashboards.filter((dashboard) => dashboard.id !== id);
    setDashboards(nextDashboards);
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(nextDashboards));
  };

  const shareDashboard = async (dashboard) => {
    try {
      await navigator.clipboard.writeText(`${window.location.origin}${dashboard.url}`);
    } catch {
      window.prompt("Copy dashboard link", `${window.location.origin}${dashboard.url}`);
    }
  };

  return (
    <section className="rounded-[28px] border border-zinc-200 bg-white/90 p-6 shadow-[0_18px_40px_rgba(15,23,42,0.08)]" data-testid="saved-dashboards-panel">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Reusable dashboards</p>
          <h3 className="mt-2 text-2xl font-medium tracking-tight text-zinc-950">Save faculty-ready analytics states</h3>
        </div>
        <div className="flex flex-col gap-3 sm:flex-row">
          <input className="h-11 rounded-full border border-zinc-200 bg-zinc-50 px-4 text-sm text-zinc-900 outline-none focus:border-zinc-900" data-testid="dashboard-name-input" onChange={(event) => setName(event.target.value)} placeholder="High Growth Startups" value={name} />
          <Button className="rounded-full bg-[#0055ff] text-white hover:bg-[#0044cc]" data-testid="dashboard-save-button" onClick={saveDashboard}>
            <BookmarkPlus className="mr-2 h-4 w-4" /> Save dashboard
          </Button>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-3 lg:grid-cols-2">
        {dashboards.length ? dashboards.map((dashboard) => (
          <div className="flex items-center justify-between gap-3 rounded-3xl border border-zinc-200 bg-zinc-50 px-4 py-4" data-testid={`saved-dashboard-item-${dashboard.id}`} key={dashboard.id}>
            <div>
              <p className="text-sm font-medium text-zinc-950">{dashboard.name}</p>
              <p className="text-xs text-zinc-500">{dashboard.url}</p>
            </div>
            <div className="flex gap-2">
              <Button className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid={`saved-dashboard-load-${dashboard.id}`} onClick={() => onApplyDashboard(dashboard)} variant="outline">
                <FolderOpen className="mr-2 h-4 w-4" /> Load
              </Button>
              <Button className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid={`saved-dashboard-share-${dashboard.id}`} onClick={() => shareDashboard(dashboard)} variant="outline">
                <Copy className="h-4 w-4" />
              </Button>
              <Button className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid={`saved-dashboard-delete-${dashboard.id}`} onClick={() => deleteDashboard(dashboard.id)} variant="outline">
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </div>
        )) : <p className="text-sm text-zinc-500">No saved dashboards yet.</p>}
      </div>
    </section>
  );
}