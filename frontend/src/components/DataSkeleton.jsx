export default function DataSkeleton({ type = "list" }) {
  if (type === "detail") {
    return (
      <div className="space-y-6" data-testid="detail-loading-skeleton">
        <div className="h-40 animate-pulse rounded-[30px] bg-zinc-100" />
        <div className="grid grid-cols-1 gap-6 xl:grid-cols-[76px_1fr]">
          <div className="hidden h-80 animate-pulse rounded-[28px] bg-zinc-100 xl:block" />
          <div className="space-y-6">
            <div className="h-32 animate-pulse rounded-[30px] bg-zinc-100" />
            <div className="h-[50vh] animate-pulse rounded-[30px] bg-zinc-100" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2 2xl:grid-cols-3" data-testid="list-loading-skeleton">
      {Array.from({ length: 6 }).map((_, index) => (
        <div className="overflow-hidden rounded-[28px] border border-zinc-200 bg-white/90 p-5 shadow-[0_18px_40px_rgba(15,23,42,0.08)]" key={index}>
          <div className="h-40 animate-pulse rounded-[22px] bg-zinc-100" />
          <div className="mt-5 h-5 w-32 animate-pulse rounded-full bg-zinc-100" />
          <div className="mt-3 h-8 w-48 animate-pulse rounded-full bg-zinc-100" />
          <div className="mt-4 h-4 w-full animate-pulse rounded-full bg-zinc-100" />
          <div className="mt-2 h-4 w-4/5 animate-pulse rounded-full bg-zinc-100" />
        </div>
      ))}
    </div>
  );
}