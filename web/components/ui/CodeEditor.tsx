"use client";

import React, { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import { RotateCcw, Type, Code } from "lucide-react";

// Dynamically import Monaco Editor to avoid SSR conflicts
const MonacoEditor = dynamic(() => import("@monaco-editor/react"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full min-h-[400px] flex items-center justify-center bg-[#0B1220] text-slate-500 font-mono text-xs">
      Loading Monaco Editor...
    </div>
  ),
});

interface CodeEditorProps {
  problemSlug: string;
  language: string;
  onLanguageChange: (lang: string) => void;
  code: string;
  onCodeChange: (code: string) => void;
  defaultStarterCodes: Record<string, string>;
}

export default function CodeEditor({
  problemSlug,
  language,
  onLanguageChange,
  code,
  onCodeChange,
  defaultStarterCodes,
}: CodeEditorProps) {
  const [fontSize, setFontSize] = useState<number>(14);

  // Restore draft from localStorage whenever slug or language changes
  useEffect(() => {
    if (typeof window === "undefined") return;
    const key = `ready2code_draft_${problemSlug}_${language}`;
    const saved = localStorage.getItem(key);
    if (saved !== null) {
      onCodeChange(saved);
    } else if (defaultStarterCodes[language]) {
      onCodeChange(defaultStarterCodes[language]);
    }
  }, [problemSlug, language]);

  const handleEditorChange = (value: string | undefined) => {
    const val = value || "";
    onCodeChange(val);
    if (typeof window !== "undefined") {
      const key = `ready2code_draft_${problemSlug}_${language}`;
      localStorage.setItem(key, val);
    }
  };

  const handleReset = () => {
    const starter = defaultStarterCodes[language] || "";
    onCodeChange(starter);
    if (typeof window !== "undefined") {
      const key = `ready2code_draft_${problemSlug}_${language}`;
      localStorage.setItem(key, starter);
    }
  };

  const monacoLanguage = language === "c++" ? "cpp" : language.toLowerCase();

  return (
    <div className="flex flex-col h-full bg-[#0B1220] rounded-xl border border-slate-800 overflow-hidden shadow-2xl">
      {/* Editor toolbar */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-[#121C2F] border-b border-slate-800 text-xs">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 text-slate-300 font-medium">
            <Code className="w-4 h-4 text-cyan-400" />
            <select
              value={language}
              onChange={(e) => onLanguageChange(e.target.value)}
              aria-label="Programming Language"
              className="bg-[#0B1220] border border-slate-700 rounded-lg px-2.5 py-1 text-slate-200 focus:outline-none focus:border-cyan-500 font-sans"
            >
              <option value="python">Python 3</option>
              <option value="javascript">JavaScript (Node.js)</option>
              <option value="c++">C++ (GCC)</option>
              <option value="java">Java (OpenJDK)</option>
            </select>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {/* Font size control */}
          <div className="flex items-center gap-1.5 bg-[#0B1220] border border-slate-700/80 rounded-lg px-2 py-0.5 text-slate-300">
            <Type className="w-3.5 h-3.5 text-slate-400" />
            <button
              onClick={() => setFontSize((prev) => Math.max(11, prev - 1))}
              className="px-1 text-slate-400 hover:text-white"
              title="Decrease font size"
            >
              -
            </button>
            <span className="font-mono text-[11px] w-4 text-center">{fontSize}</span>
            <button
              onClick={() => setFontSize((prev) => Math.min(22, prev + 1))}
              className="px-1 text-slate-400 hover:text-white"
              title="Increase font size"
            >
              +
            </button>
          </div>

          {/* Reset button */}
          <button
            onClick={handleReset}
            className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors border border-slate-700 text-[11px]"
            title="Reset code to default template"
          >
            <RotateCcw className="w-3 h-3" />
            <span>Reset</span>
          </button>
        </div>
      </div>

      {/* Editor container */}
      <div className="flex-1 w-full min-h-[450px]">
        <MonacoEditor
          height="100%"
          language={monacoLanguage}
          value={code}
          theme="vs-dark"
          onChange={handleEditorChange}
          options={{
            fontSize: fontSize,
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 4,
            padding: { top: 12, bottom: 12 },
            lineNumbers: "on",
            renderLineHighlight: "all",
            fontFamily: "'Fira Code', 'JetBrains Mono', Consolas, monospace",
            fontLigatures: true,
          }}
        />
      </div>
    </div>
  );
}
