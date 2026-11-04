"use client";

import React, { useState, useEffect, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Html, OrbitControls } from "@react-three/drei";
import { Play, Pause, SkipBack, SkipForward, RotateCcw, Volume2, Sparkles } from "lucide-react";
import * as THREE from "three";

export interface TraceFrame {
  step: number;
  array?: number[];
  pointers?: Record<string, number>;
  map?: Record<string, number>;
  highlight?: number[];
  found?: number[];
  note: string;
}

export interface TraceData {
  algo: string;
  version: number;
  scene: string;
  input: any;
  frames: TraceFrame[];
}

function ArrayPillar({
  value,
  index,
  total,
  isHighlighted,
  isFound,
  pointerName,
}: {
  value: number;
  index: number;
  total: number;
  isHighlighted: boolean;
  isFound: boolean;
  pointerName?: string;
}) {
  const height = Math.max(0.6, (value / 15) * 3);
  const x = (index - total / 2 + 0.5) * 1.35;
  const meshRef = useRef<THREE.Mesh>(null);

  return (
    <group position={[x, height / 2, 0]}>
      {/* 3D Pillar */}
      <mesh ref={meshRef}>
        <boxGeometry args={[0.9, height, 0.9]} />
        <meshStandardMaterial
          color={
            isFound
              ? "#22C55E"
              : isHighlighted
              ? "#22D3EE"
              : "#1E293B"
          }
          emissive={isFound ? "#22C55E" : isHighlighted ? "#0284C7" : "#0F172A"}
          emissiveIntensity={isFound ? 0.8 : isHighlighted ? 0.6 : 0.1}
          roughness={0.25}
          metalness={0.6}
        />
      </mesh>

      {/* Value label on pillar top */}
      <Html position={[0, height / 2 + 0.35, 0]} center>
        <div
          className={`px-2 py-0.5 rounded text-[11px] font-mono font-bold shadow-md select-none ${
            isFound
              ? "bg-emerald-500 text-slate-950 ring-2 ring-emerald-300"
              : isHighlighted
              ? "bg-cyan-400 text-slate-950 ring-2 ring-cyan-200"
              : "bg-slate-800 text-slate-200 border border-slate-700"
          }`}
        >
          {value}
        </div>
      </Html>

      {/* Pointer indicator arrow */}
      {pointerName && (
        <Html position={[0, height / 2 + 0.9, 0]} center>
          <div className="flex flex-col items-center">
            <span className="px-1.5 py-0.5 rounded bg-violet-500 text-white font-mono text-[10px] font-extrabold shadow">
              {pointerName}
            </span>
            <span className="text-violet-400 font-bold -mt-1 text-xs">&darr;</span>
          </div>
        </Html>
      )}

      {/* Index label on floor */}
      <Html position={[0, -height / 2 - 0.25, 0]} center>
        <span className="text-[10px] font-mono text-slate-500">[{index}]</span>
      </Html>
    </group>
  );
}

function FloatingMapCard({ mapData }: { mapData?: Record<string, number> }) {
  if (!mapData || Object.keys(mapData).length === 0) return null;

  return (
    <Html position={[0, 3.2, -1.5]} center>
      <div className="p-3 rounded-xl bg-[#121C2F]/90 backdrop-blur-md border border-cyan-500/30 shadow-2xl min-w-[200px]">
        <div className="text-[10px] uppercase font-mono font-bold tracking-wider text-cyan-400 mb-1.5 flex items-center gap-1">
          <Sparkles className="w-3 h-3" /> Hash Map [Value &rarr; Index]
        </div>
        <div className="flex flex-wrap gap-1.5">
          {Object.entries(mapData).map(([k, v]) => (
            <span
              key={k}
              className="px-2 py-0.5 rounded-md bg-[#0B1220] border border-cyan-400/40 text-cyan-200 font-mono text-xs"
            >
              {k}: <span className="text-violet-400 font-bold">{v}</span>
            </span>
          ))}
        </div>
      </div>
    </Html>
  );
}

export default function Visualizer3D({ trace }: { trace: TraceData }) {
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState<number>(1);
  const [hasWebGL, setHasWebGL] = useState(true);

  const totalSteps = trace.frames.length;
  const frame = trace.frames[currentStep] || trace.frames[0];

  useEffect(() => {
    try {
      const c = document.createElement("canvas");
      setHasWebGL(Boolean(c.getContext("webgl") || c.getContext("experimental-webgl")));
    } catch {
      setHasWebGL(false);
    }
  }, []);

  // Keyboard navigation: Space = Play/Pause, Left/Right = Prev/Next, 1-3 = Speed
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;

      if (e.code === "Space") {
        e.preventDefault();
        setIsPlaying((p) => !p);
      } else if (e.code === "ArrowLeft") {
        e.preventDefault();
        setCurrentStep((s) => Math.max(0, s - 1));
      } else if (e.code === "ArrowRight") {
        e.preventDefault();
        setCurrentStep((s) => Math.min(totalSteps - 1, s + 1));
      } else if (e.key === "1") {
        setSpeed(0.5);
      } else if (e.key === "2") {
        setSpeed(1);
      } else if (e.key === "3") {
        setSpeed(2);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [totalSteps]);

  // Autoplay loop
  useEffect(() => {
    if (!isPlaying) return;
    const intervalMs = 1200 / speed;
    const timer = setInterval(() => {
      setCurrentStep((s) => {
        if (s >= totalSteps - 1) {
          setIsPlaying(false);
          return s;
        }
        return s + 1;
      });
    }, intervalMs);
    return () => clearInterval(timer);
  }, [isPlaying, speed, totalSteps]);

  const array = frame.array || trace.input?.nums || [2, 7, 11, 15];

  return (
    <div className="flex flex-col gap-4 bg-[#121C2F] rounded-2xl border border-slate-800 p-6 shadow-2xl">
      {/* 3D Stage Canvas */}
      <div className="relative w-full h-[380px] bg-[#0B1220] rounded-xl border border-slate-800/80 overflow-hidden">
        {hasWebGL ? (
          <Canvas
            camera={{ position: [0, 2.5, 6.5], fov: 45 }}
            dpr={[1, 1.5]}
            gl={{ antialias: true }}
          >
            <ambientLight intensity={0.8} />
            <pointLight position={[5, 10, 5]} intensity={1.5} color="#22D3EE" />
            <pointLight position={[-5, 5, -5]} intensity={1} color="#8B5CF6" />

            {/* Grid Floor */}
            <gridHelper args={[16, 16, "#1E293B", "#0E1726"]} position={[0, -0.01, 0]} />

            {/* Array Pillars */}
            {array.map((val: number, idx: number) => {
              const isHigh = frame.highlight?.includes(idx) || false;
              const isFound = frame.found?.includes(idx) || false;
              let pointer = "";
              if (frame.pointers) {
                for (const [pName, pIdx] of Object.entries(frame.pointers)) {
                  if (pIdx === idx) pointer = pName;
                }
              }
              return (
                <ArrayPillar
                  key={idx}
                  value={val}
                  index={idx}
                  total={array.length}
                  isHighlighted={isHigh}
                  isFound={isFound}
                  pointerName={pointer || undefined}
                />
              );
            })}

            {/* Floating Hash Map if scene uses it */}
            {frame.map && <FloatingMapCard mapData={frame.map} />}

            <OrbitControls enablePan={false} maxPolarAngle={Math.PI / 2.1} minPolarAngle={Math.PI / 4} />
          </Canvas>
        ) : (
          <div className="w-full h-full flex items-center justify-center text-slate-400">
            WebGL is not active. Use the step text and transport controls below.
          </div>
        )}
      </div>

      {/* Screen reader live region & explanatory note */}
      <div
        role="status"
        aria-live="polite"
        className="p-3 rounded-xl bg-[#0B1220] border border-cyan-500/20 text-slate-200 text-sm flex items-start gap-2.5 font-sans"
      >
        <Volume2 className="w-4 h-4 text-cyan-400 mt-0.5 shrink-0" />
        <div>
          <span className="font-bold text-cyan-400 mr-2">Step {frame.step + 1} of {totalSteps}:</span>
          <span>{frame.note}</span>
        </div>
      </div>

      {/* Transport Controls Bar (Play, Pause, Step, Scrub, Speed) */}
      <div className="flex flex-wrap items-center justify-between gap-4 pt-2 border-t border-slate-800">
        <div className="flex items-center gap-2">
          {/* Reset */}
          <button
            onClick={() => {
              setIsPlaying(false);
              setCurrentStep(0);
            }}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
            title="Reset to beginning"
            aria-label="Reset to beginning"
          >
            <RotateCcw className="w-4 h-4" />
          </button>

          {/* Prev */}
          <button
            onClick={() => setCurrentStep((s) => Math.max(0, s - 1))}
            disabled={currentStep === 0}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 disabled:opacity-40 transition-colors"
            title="Previous Step (Left Arrow)"
            aria-label="Previous Step"
          >
            <SkipBack className="w-4 h-4" />
          </button>

          {/* Play/Pause */}
          <button
            onClick={() => setIsPlaying((p) => !p)}
            className="px-4 py-2 rounded-lg bg-cyan-400 hover:bg-cyan-300 text-slate-950 font-bold flex items-center gap-1.5 shadow-lg shadow-cyan-500/20 transition-all"
            title="Play / Pause (Space)"
            aria-label={isPlaying ? "Pause animation" : "Play animation"}
          >
            {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 fill-slate-950" />}
            <span>{isPlaying ? "Pause" : "Play"}</span>
          </button>

          {/* Next */}
          <button
            onClick={() => setCurrentStep((s) => Math.min(totalSteps - 1, s + 1))}
            disabled={currentStep === totalSteps - 1}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 disabled:opacity-40 transition-colors"
            title="Next Step (Right Arrow)"
            aria-label="Next Step"
          >
            <SkipForward className="w-4 h-4" />
          </button>
        </div>

        {/* Scrub Slider */}
        <div className="flex-1 min-w-[200px] flex items-center gap-3">
          <input
            type="range"
            min={0}
            max={totalSteps - 1}
            value={currentStep}
            onChange={(e) => {
              setIsPlaying(false);
              setCurrentStep(parseInt(e.target.value));
            }}
            className="w-full accent-cyan-400 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
          />
          <span className="font-mono text-xs text-slate-400 w-12 text-right">
            {currentStep + 1} / {totalSteps}
          </span>
        </div>

        {/* Speed Selector */}
        <div className="flex items-center gap-1 bg-[#0B1220] p-1 rounded-lg border border-slate-800 text-xs">
          {[0.5, 1, 2].map((s) => (
            <button
              key={s}
              onClick={() => setSpeed(s)}
              className={`px-2.5 py-1 rounded font-mono font-medium transition-colors ${
                speed === s
                  ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              {s}x
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
