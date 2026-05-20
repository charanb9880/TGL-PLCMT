import { useEffect, useState } from "react";
import { BookmarkPlus, FolderOpen, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/button";


const STORAGE_KEY = "placement-filter-presets-v1";


export default function SavedFilterPresets({ filters, onApplyPreset }) {
  const [name, setName] = useState("");
  const [presets, setPresets] = useState([]);

  useEffect(() => {
    setPresets(JSON.parse(window.localStorage.getItem(STORAGE_KEY) || "[]"));
  }, []);

  const savePreset = () => {
    if (!name.trim()) {
      return;
    }
    const nextPresets = [
      { id: Date.now(), name: name.trim(), filters },
      ...presets,
    ];
    setPresets(nextPresets);
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(nextPresets));
    setName("");
  };

  const deletePreset = (id) => {
    const nextPresets = presets.filter((preset) => preset.id !== id);
    setPresets(nextPresets);
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(nextPresets));
  };

  return (
    <section className="rounded-[28px] border border-zinc-200 bg-white/90 p-6 shadow-[0_18px_40px_rgba(15,23,42,0.08)]" data-testid="saved-filter-presets-panel">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Faculty presets</p>
          <h3 className="mt-2 text-2xl font-medium tracking-tight text-zinc-950">Save and reload filter combinations</h3>
        </div>
        <div className="flex flex-col gap-3 sm:flex-row">
          <input
            className="h-11 rounded-full border border-zinc-200 bg-zinc-50 px-4 text-sm text-zinc-900 outline-none focus:border-zinc-900"
            data-testid="filter-preset-name-input"
            onChange={(event) => setName(event.target.value)}
            placeholder="Example: Top Product Companies"
            value={name}
          />
          <Button className="rounded-full bg-[#0055ff] text-white hover:bg-[#0044cc]" data-testid="filter-preset-save-button" onClick={savePreset}>
            <BookmarkPlus className="mr-2 h-4 w-4" /> Save preset
          </Button>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-3 lg:grid-cols-2">
        {presets.length ? presets.map((preset) => (
          <div className="flex items-center justify-between gap-3 rounded-3xl border border-zinc-200 bg-zinc-50 px-4 py-4" data-testid={`filter-preset-item-${preset.id}`} key={preset.id}>
            <div>
              <p className="text-sm font-medium text-zinc-950">{preset.name}</p>
              <p className="text-xs text-zinc-500">{Object.entries(preset.filters || {}).filter(([, value]) => value).length} saved filters</p>
            </div>
            <div className="flex gap-2">
              <Button className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid={`filter-preset-load-${preset.id}`} onClick={() => onApplyPreset(preset.filters)} variant="outline">
                <FolderOpen className="mr-2 h-4 w-4" /> Load
              </Button>
              <Button className="rounded-full border-zinc-300 bg-white text-zinc-900 hover:bg-zinc-100" data-testid={`filter-preset-delete-${preset.id}`} onClick={() => deletePreset(preset.id)} variant="outline">
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </div>
        )) : <p className="text-sm text-zinc-500">No saved filter presets yet.</p>}
      </div>
    </section>
  );
}