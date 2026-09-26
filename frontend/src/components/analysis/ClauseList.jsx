import React, { useState, useMemo } from "react";
import { ClauseCard } from "./ClauseCard";
import { Search, ArrowUpDown, Filter } from "lucide-react";

export function ClauseList({ clauses = [], selectedClauseId, onSelectClause }) {
  const [filter, setFilter] = useState("all");
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState("index"); // 'index' or 'risk'

  const filteredClauses = useMemo(() => {
    return clauses
      .filter((c) => {
        if (filter !== "all" && c.favorability_label !== filter) return false;
        if (search) {
          const q = search.toLowerCase();
          const matchType = (c.clause_type || "").toLowerCase().includes(q);
          const matchText = (c.redacted_text || "").toLowerCase().includes(q);
          if (!matchType && !matchText) return false;
        }
        return true;
      })
      .sort((a, b) => {
        if (sortBy === "risk") {
          return (b.risk_score || 0) - (a.risk_score || 0);
        }
        return a.clause_index - b.clause_index;
      });
  }, [clauses, filter, search, sortBy]);

  return (
    <div className="space-y-4">
      {/* Controls Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 border border-white/20 bg-paper-dim p-4">
        {/* Search */}
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search clauses or keywords..."
            className="w-full bg-black border border-rule pl-9 pr-3 py-2 text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-white"
          />
        </div>

        {/* Filter Buttons */}
        <div className="flex items-center gap-1 overflow-x-auto">
          {["all", "unfavorable", "needs_review", "fair"].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1.5 text-[11px] font-mono uppercase tracking-wider border whitespace-nowrap transition-colors ${
                filter === f
                  ? "border-white bg-white text-black font-bold"
                  : "border-rule bg-black text-zinc-400 hover:text-white hover:border-white/40"
              }`}
            >
              {f.replace("_", " ")}
            </button>
          ))}

          {/* Sort button */}
          <button
            onClick={() => setSortBy(sortBy === "index" ? "risk" : "index")}
            className="px-3 py-1.5 text-[11px] font-mono uppercase tracking-wider border border-rule bg-black text-zinc-400 hover:text-white flex items-center gap-1.5"
            title="Toggle sort order"
          >
            <ArrowUpDown className="w-3 h-3" />
            {sortBy === "risk" ? "Risk Score" : "Document Order"}
          </button>
        </div>
      </div>

      {/* Clause Cards */}
      {filteredClauses.length > 0 ? (
        <div className="space-y-3">
          {filteredClauses.map((clause) => (
            <ClauseCard
              key={clause.id}
              clause={clause}
              isSelected={selectedClauseId === clause.id}
              onSelect={() => onSelectClause(clause.id)}
            />
          ))}
        </div>
      ) : (
        <div className="border border-rule bg-paper-dim p-8 text-center text-zinc-500 text-xs font-mono">
          No clauses match the selected search or filter criteria.
        </div>
      )}
    </div>
  );
}
