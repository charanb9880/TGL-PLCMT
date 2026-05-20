import { AlertCircle, LoaderCircle } from "lucide-react";

import { Button } from "@/components/ui/button";


export default function PageState({ actionLabel, description, loading = false, onAction, testId, title }) {
  return (
    <div className="flex min-h-[50vh] items-center justify-center" data-testid={testId}>
      <div className="max-w-xl rounded-[32px] border border-zinc-200 bg-white/90 px-8 py-10 text-center shadow-[0_18px_50px_rgba(15,23,42,0.08)]">
        <div className="mx-auto mb-5 flex h-14 w-14 items-center justify-center rounded-2xl border border-zinc-200 bg-zinc-50">
          {loading ? <LoaderCircle className="h-6 w-6 animate-spin text-[#0055ff]" /> : <AlertCircle className="h-6 w-6 text-[#0055ff]" />}
        </div>
        <p className="text-xs font-bold uppercase tracking-[0.28em] text-zinc-500">{loading ? "Loading" : "Status"}</p>
        <h2 className="mt-2 text-3xl font-medium tracking-tight text-zinc-950">{title}</h2>
        <p className="mt-3 text-sm leading-relaxed text-zinc-600">{description}</p>
        {!loading && actionLabel && onAction ? (
          <Button className="mt-6 rounded-full bg-[#0055ff] px-6 text-white hover:bg-[#0044cc]" data-testid={`${testId}-action`} onClick={onAction}>
            {actionLabel}
          </Button>
        ) : null}
      </div>
    </div>
  );
}