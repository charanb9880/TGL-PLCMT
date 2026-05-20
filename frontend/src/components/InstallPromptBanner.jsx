import { useEffect, useState } from "react";
import { Download } from "lucide-react";

import { Button } from "@/components/ui/button";


export default function InstallPromptBanner() {
  const [promptEvent, setPromptEvent] = useState(null);

  useEffect(() => {
    const handleBeforeInstallPrompt = (event) => {
      event.preventDefault();
      setPromptEvent(event);
    };

    window.addEventListener("beforeinstallprompt", handleBeforeInstallPrompt);
    return () => window.removeEventListener("beforeinstallprompt", handleBeforeInstallPrompt);
  }, []);

  if (!promptEvent) {
    return null;
  }

  return (
    <div className="mt-6 flex items-center justify-between gap-4 rounded-[24px] border border-zinc-200 bg-white/90 px-5 py-4 shadow-[0_18px_40px_rgba(15,23,42,0.08)]" data-testid="install-prompt-banner">
      <div>
        <p className="text-xs font-bold uppercase tracking-[0.24em] text-zinc-500">Installable PWA</p>
        <p className="mt-1 text-sm text-zinc-700">Add Placement Intelligence to the home screen for faster access and offline fallback.</p>
      </div>
      <Button className="rounded-full bg-[#0055ff] text-white hover:bg-[#0044cc]" data-testid="install-prompt-button" onClick={async () => {
        await promptEvent.prompt();
        setPromptEvent(null);
      }}>
        <Download className="mr-2 h-4 w-4" /> Install app
      </Button>
    </div>
  );
}