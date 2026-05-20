import { useEffect, useState } from "react";
import { BookmarkPlus, FolderOpen, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/button";


const STORAGE_KEY = "placement-comparison-workspaces-v1";


export default function SavedComparisonWorkspaces({ comparison, leftCompanyId, onLoadWorkspace, rightCompanyId }) {
  const [name, setName] = useState("");
  const [workspaces, setWorkspaces] = useState([]);

  useEffect(() => {
    setWorkspaces(JSON.parse(window.localStorage.getItem(STORAGE_KEY) || "[]"));
  }, []);

  const saveWorkspace = () => {
    if (!comparison || !name.trim()) {
      return;
    }

    const nextWorkspaces = [
      {
        id: Date.now(),
        name: name.trim(),
        leftCompanyId,
        rightCompanyId,
        url: `/compare?c1=${leftCompanyId}&c2=${rightCompanyId}`,
        comparison,
      },
      ...workspaces,
    ];
    setWorkspaces(nextWorkspaces);
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(nextWorkspaces));
    setName("");
  };

  const deleteWorkspace = (id) => {
    const nextWorkspaces = workspaces.filter((workspace) => workspace.id !== id);
    setWorkspaces(nextWorkspaces);
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(nextWorkspaces));
  };

  return (
    <section className="rounded-[28px] border border-zinc-200 bg-white/90 p-6 shadow-[0_18px_40px_rgba(15,23,42,0.08)]" data-testid="saved-comparison-workspaces-panel">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Saved workspaces</p>
          <h3 className="mt-2 text-2xl font-medium tracking-tight text-zinc-950">Store reusable comparison setups</h3>
        </div>
        <div className="flex flex-col gap-3 sm:flex-row">
          <input
            className="h-11 rounded-full border border-zinc-200 bg-zinc-50 px-4 text-sm text-zinc-900 outline-none focus:border-zinc-900"
            data-testid="comparison-workspace-name-input"
            onChange={(event) => setName(event.target.value)}
            placeholder="Example: Startup vs Service"
            value={name}
          />
          <Button className="rounded-full bg-[#0055ff] text-white hover:bg-[#0044cc]" data-testid="comparison-workspace-save-button" disabled={!comparison} onClick={saveWorkspace}>
            <BookmarkPlus className="mr-2 h-4 w-4" /> Save workspace
          </Button>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-3 lg:grid-cols-2">
        {workspaces.length ? workspaces.map((workspace) => (
          <div className="flex items-center justify-between gap-3 rounded-3xl border border-zinc-200 bg-zinc-50 px-4 py-4" data-testid={`comparison-workspace-item-${workspace.id}`} key={workspace.id}>
            <div>
              <p className="text-sm font-medium text-zinc-950">{workspace.name}</p>
              <p className="text-xs text-zinc-500">{workspace.url}</p>
            </div>
            <div className="flex gap-2">
              <Button className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid={`comparison-workspace-load-${workspace.id}`} onClick={() => onLoadWorkspace(workspace)} variant="outline">
                <FolderOpen className="mr-2 h-4 w-4" /> Load
              </Button>
              <Button className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid={`comparison-workspace-delete-${workspace.id}`} onClick={() => deleteWorkspace(workspace.id)} variant="outline">
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </div>
        )) : <p className="text-sm text-zinc-500">No saved comparison workspaces yet.</p>}
      </div>
    </section>
  );
}