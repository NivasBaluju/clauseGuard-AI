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
      <label className="block text-xs font-mono uppercase tracking-wider text-neutral-600 font-semibold">
        1. Select Document Type <span className="text-red-600">* (Required)</span>
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
                  ? "border-black bg-black text-white"
                  : "border-neutral-200 bg-white text-neutral-800 hover:border-neutral-400 shadow-sm"
              }`}
            >
              <div className="flex items-center justify-between mb-3">
                <Icon className={`w-5 h-5 ${isSelected ? "text-white" : "text-black"}`} />
                <span
                  className={`w-3.5 h-3.5 border flex items-center justify-center ${
                    isSelected ? "border-white bg-white" : "border-neutral-400 bg-white"
                  }`}
                >
                  {isSelected && <span className="w-1.5 h-1.5 bg-black" />}
                </span>
              </div>
              <h4 className={`font-serif text-base font-bold mb-1 ${isSelected ? "text-white" : "text-black"}`}>
                {type.title}
              </h4>
              <p className={`text-xs mb-2 font-sans leading-relaxed ${isSelected ? "text-neutral-300" : "text-neutral-600"}`}>
                {type.subtitle}
              </p>
              <p className={`text-[11px] leading-normal border-t pt-2 ${isSelected ? "border-neutral-700 text-neutral-300" : "border-neutral-200 text-neutral-500"}`}>
                {type.description}
              </p>
            </button>
          );
        })}
      </div>
    </div>
  );
}
