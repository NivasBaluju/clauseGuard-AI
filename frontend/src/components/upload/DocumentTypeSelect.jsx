import React from "react";
import { Home, Briefcase, FileCheck } from "lucide-react";

export const DOCUMENT_TYPES = [
  {
    id: "rental_agreement",
    title: "Rental / Lease Agreement",
    subtitle: "Residential leases, tenancy contracts, room rentals",
    icon: Home,
    description: "Evaluates security deposits, late fee structures, maintenance covenants, and termination rights against standard residential protections.",
  },
  {
    id: "job_offer_letter",
    title: "Job Offer Letter",
    subtitle: "Employment offers, executive compensation, at-will agreements",
    icon: Briefcase,
    description: "Scrutinizes non-compete/non-solicit covenants, IP assignment overbreadth, severance terms, and bonus/equity vesting schedules.",
  },
  {
    id: "insurance_policy",
    title: "Insurance Policy (Renters/Homeowners)",
    subtitle: "ISO HO-4 broad form, property & casualty policy forms",
    icon: FileCheck,
    description: "Detects hidden coverage exclusions, strict claim notice windows, liability limits, and cancellation/grace period terms.",
  },
];

export function DocumentTypeSelect({ value, onChange }) {
  return (
    <div className="space-y-3">
      <label className="block text-xs font-mono uppercase tracking-wider text-zinc-400">
        1. Select Document Type <span className="text-red-500">* (Required)</span>
      </label>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {DOCUMENT_TYPES.map((type) => {
          const Icon = type.icon;
          const isSelected = value === type.id;
          return (
            <button
              key={type.id}
              type="button"
              onClick={() => onChange(type.id)}
              className={`p-5 text-left border transition-all ${
                isSelected
                  ? "border-white bg-white/10 text-white"
                  : "border-rule bg-paper-dim text-zinc-400 hover:border-white/30 hover:text-white"
              }`}
            >
              <div className="flex items-center justify-between mb-3">
                <Icon className={`w-5 h-5 ${isSelected ? "text-white" : "text-zinc-500"}`} />
                <span
                  className={`w-3.5 h-3.5 border flex items-center justify-center ${
                    isSelected ? "border-white bg-white" : "border-zinc-600"
                  }`}
                >
                  {isSelected && <span className="w-1.5 h-1.5 bg-black" />}
                </span>
              </div>
              <h4 className="font-serif text-base font-bold text-white mb-1">
                {type.title}
              </h4>
              <p className="text-xs text-zinc-400 mb-2 font-sans leading-relaxed">
                {type.subtitle}
              </p>
              <p className="text-[11px] text-zinc-500 leading-normal border-t border-rule pt-2">
                {type.description}
              </p>
            </button>
          );
        })}
      </div>
    </div>
  );
}
