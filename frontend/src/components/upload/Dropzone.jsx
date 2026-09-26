import React, { useRef, useState } from "react";
import { Upload, FileText, CheckCircle2, AlertCircle, X } from "lucide-react";

export function Dropzone({ file, onFileSelect, onClearFile, error }) {
  const [isDragOver, setIsDragOver] = useState(false);
  const inputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      onFileSelect(e.target.files[0]);
    }
  };

  return (
    <div className="space-y-3">
      <label className="block text-xs font-mono uppercase tracking-wider text-zinc-400">
        2. Upload Document File <span className="text-zinc-500">(.pdf, .docx, .txt — Max 20MB)</span>
      </label>

      {!file ? (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
          className={`border-2 border-dashed p-10 text-center cursor-pointer transition-all ${
            isDragOver
              ? "border-white bg-white/5"
              : error
              ? "border-red-500/50 bg-red-950/10"
              : "border-rule hover:border-white/40 bg-paper-dim"
          }`}
        >
          <input
            ref={inputRef}
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={handleFileChange}
            className="hidden"
          />
          <div className="w-12 h-12 border border-rule mx-auto mb-4 flex items-center justify-center text-zinc-400">
            <Upload className="w-5 h-5" />
          </div>
          <p className="font-serif text-lg text-white mb-1">
            Drag & drop legal document here
          </p>
          <p className="text-xs text-zinc-400 font-sans mb-4">
            or click to browse your computer
          </p>
          <span className="inline-block text-[11px] font-mono text-zinc-500 border border-rule px-3 py-1">
            DIGITAL OR SCANNED PDF • WORD DOCX • PLAIN TXT
          </span>

          {error && (
            <p className="text-xs text-red-400 mt-3 flex items-center justify-center gap-1.5 font-mono">
              <AlertCircle className="w-3.5 h-3.5" />
              {error}
            </p>
          )}
        </div>
      ) : (
        <div className="border border-white/20 bg-paper-dim p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 border border-white/20 bg-white/5 flex items-center justify-center text-white">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <p className="text-sm font-bold text-white font-mono">{file.name}</p>
              <p className="text-xs text-zinc-400 font-mono">
                {(file.size / (1024 * 1024)).toFixed(2)} MB • {file.name.split(".").pop().toUpperCase()}
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClearFile}
            className="p-1.5 border border-rule hover:border-white/40 text-zinc-400 hover:text-white"
            aria-label="Remove file"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  );
}
