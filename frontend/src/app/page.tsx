"use client";

import { useState } from "react";
import ImageUpload from "@/components/upload/ImageUpload";
import AnalysisResult from "@/components/results/AnalysisResult";
import { analyzeImage } from "@/lib/api";
import { AnalysisResponse } from "@/types";

export default function HomePage() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [fileName, setFileName] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function handleUpload(file: File) {
    setIsLoading(true);
    setError(null);
    setResult(null);
    setFileName(file.name);

    try {
      const data = await analyzeImage(file);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="max-w-2xl mx-auto px-4 py-16 space-y-10">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900">MicroQuant</h1>
          <p className="text-gray-500">Automated bacterial colony detection and counting.</p>
        </div>

        {/* Upload */}
        <ImageUpload onUpload={handleUpload} isLoading={isLoading} />

        {/* Loading */}
        {isLoading && (
          <div className="flex justify-center">
            <div className="flex items-center gap-2 text-sm text-gray-500">
              <svg className="animate-spin w-4 h-4 text-blue-500" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Running analysis…
            </div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}

        {/* Result */}
        {result && !isLoading && (
          <AnalysisResult result={result} fileName={fileName} />
        )}
      </div>
    </main>
  );
}
