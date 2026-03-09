"use client";

import { useRef, useState, DragEvent, ChangeEvent } from "react";

interface ImageUploadProps {
  onUpload: (file: File) => void;
  isLoading: boolean;
}

const ACCEPTED_TYPES = ["image/png", "image/jpeg", "image/tiff"];

export default function ImageUpload({ onUpload, isLoading }: ImageUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function validate(file: File): boolean {
    if (!ACCEPTED_TYPES.includes(file.type)) {
      setError("Unsupported file type. Please upload PNG, JPEG, or TIFF.");
      return false;
    }
    setError(null);
    return true;
  }

  function handleFile(file: File) {
    if (validate(file)) onUpload(file);
  }

  function handleChange(e: ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  }

  function handleDrop(e: DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) handleFile(file);
  }

  return (
    <div className="w-full">
      <div
        onClick={() => !isLoading && inputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={`
          flex flex-col items-center justify-center gap-3
          border-2 border-dashed rounded-2xl p-12 cursor-pointer
          transition-colors duration-200
          ${isDragging ? "border-blue-500 bg-blue-50" : "border-gray-300 hover:border-blue-400 hover:bg-gray-50"}
          ${isLoading ? "opacity-50 cursor-not-allowed" : ""}
        `}
      >
        <svg className="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
            d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
        </svg>
        <div className="text-center">
          <p className="text-sm font-medium text-gray-700">
            {isLoading ? "Analyzing…" : "Drop a petri dish image here"}
          </p>
          <p className="text-xs text-gray-400 mt-1">PNG, JPEG, or TIFF</p>
        </div>
      </div>

      <input
        ref={inputRef}
        type="file"
        accept=".png,.jpg,.jpeg,.tif,.tiff"
        className="hidden"
        onChange={handleChange}
        disabled={isLoading}
      />

      {error && (
        <p className="mt-2 text-sm text-red-500">{error}</p>
      )}
    </div>
  );
}
