import { useState } from "react";
import { motion } from "framer-motion";
import { Sparkles, BrainCircuit, CheckCircle2, AlertCircle, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import CompanyCard from "@/components/CompanyCard";

const ResearchPage = () => {
  const [companyName, setCompanyName] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleResearch = async () => {
    if (!companyName.trim()) return;
    
    setLoading(true);
    setResult(null);
    setError(null);
    
    try {
      // POST to our new synchronous FastAPI endpoint
      const response = await fetch("http://localhost:8001/v1/agent/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ company_name: companyName })
      });
      
      if (!response.ok) {
        throw new Error(`Failed to generate intelligence (Status: ${response.status})`);
      }
      
      const data = await response.json();
      
      // Save the generated intelligence directly to the database
      if (data.golden_record) {
        try {
          const saveResponse = await fetch("http://localhost:8000/api/companies/save_generated", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ golden_record: data.golden_record })
          });
          
          if (saveResponse.ok) {
            const saveData = await saveResponse.json();
            data.golden_record.company_id = saveData.company_id;
          }
        } catch (saveErr) {
          console.error("Failed to persist to database:", saveErr);
        }
      }
      
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <div className="flex items-center gap-3">
        <div className="flex h-12 w-12 items-center justify-center rounded-2xl border border-zinc-200 bg-white shadow-sm">
          <BrainCircuit className="h-6 w-6 text-[#0055ff]" />
        </div>
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-500">Live Agent Pipeline</p>
          <h1 className="text-3xl font-medium tracking-tight text-zinc-950">Company Research</h1>
        </div>
      </div>

      <div className="rounded-[32px] border border-zinc-200 bg-white p-8 shadow-[0_24px_80px_rgba(15,23,42,0.06)]">
        <div className="max-w-2xl space-y-6">
          <p className="text-zinc-600">
            Enter a company name below to trigger the multi-LLM LangGraph pipeline. It will actively research the internet, run parallel agent validations, consolidate findings, and return a completely populated 163-parameter Golden Record.
          </p>
          
          <div className="flex items-center gap-4">
            <Input 
              className="h-14 flex-1 rounded-2xl border-zinc-300 bg-zinc-50 px-4 text-base"
              placeholder="e.g. OpenAI, Tesla, Stripe" 
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleResearch()}
              disabled={loading}
            />
            <Button 
              className="h-14 rounded-2xl bg-[#0055ff] px-8 text-white hover:bg-[#0044cc]"
              onClick={handleResearch}
              disabled={loading || !companyName.trim()}
            >
              {loading ? <Loader2 className="mr-2 h-5 w-5 animate-spin" /> : <Sparkles className="mr-2 h-5 w-5" />}
              {loading ? "Researching..." : "Generate Intelligence"}
            </Button>
          </div>
        </div>
      </div>

      {error && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="flex items-center gap-3 rounded-2xl bg-red-50 p-4 text-red-600 border border-red-100">
          <AlertCircle className="h-5 w-5" />
          <p className="text-sm font-medium">{error}</p>
        </motion.div>
      )}

      {loading && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex flex-col items-center justify-center py-20">
          <Loader2 className="h-10 w-10 animate-spin text-[#0055ff] mb-6" />
          <p className="text-lg font-medium text-zinc-950">Running Parallel LangGraph Agents...</p>
          <p className="text-zinc-500 mt-2">This is a synchronous request. It will block until all 163 fields are extracted and validated.</p>
        </motion.div>
      )}

      {result && result.golden_record && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
          <div className="flex items-center justify-between rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-green-50 text-green-600">
                <CheckCircle2 className="h-6 w-6" />
              </div>
              <div>
                <h3 className="text-lg font-medium text-zinc-950">Extraction Complete</h3>
                <p className="text-sm text-zinc-500">Run ID: {result.run_id}</p>
              </div>
            </div>
            {result.confidence_score !== undefined && (
              <div className="text-right">
                <p className="text-3xl font-bold text-zinc-950">{result.confidence_score}%</p>
                <p className="text-xs font-bold uppercase tracking-wider text-zinc-500">Data Confidence</p>
              </div>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <CompanyCard company={result.golden_record} />
            <div className="rounded-[32px] border border-zinc-200 bg-zinc-50 p-8 shadow-sm flex flex-col justify-center items-center text-center space-y-4">
              <Sparkles className="h-10 w-10 text-[#0055ff]" />
              <h3 className="text-2xl font-medium text-zinc-900">Golden Record Generated</h3>
              <p className="text-zinc-600">All 163 parameters have been extracted successfully. The preview card on the left uses the same exact component as the Home page.</p>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
}

export default ResearchPage;
