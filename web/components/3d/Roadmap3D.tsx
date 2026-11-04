"use client";

import React, { useState, useRef, useEffect } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Html, Float, OrbitControls } from "@react-three/drei";
import { Lock, CheckCircle2, ChevronRight, Sparkles } from "lucide-react";
import * as THREE from "three";

export interface RoadmapTopic {
  id: string;
  slug: string;
  name: string;
  totalProblems: number;
  solvedCount: number;
  order: number;
}

interface Roadmap3DProps {
  topics: RoadmapTopic[];
  onSelectTopic: (topic: RoadmapTopic) => void;
  selectedTopicSlug?: string;
}

function IslandMesh({
  topic,
  position,
  isUnlocked,
  isCompleted,
  isSelected,
  onClick,
}: {
  topic: RoadmapTopic;
  position: [number, number, number];
  isUnlocked: boolean;
  isCompleted: boolean;
  isSelected: boolean;
  onClick: () => void;
}) {
  const meshRef = useRef<THREE.Group>(null);
  const [hovered, setHovered] = useState(false);

  useFrame((state, delta) => {
    if (meshRef.current && isUnlocked) {
      meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime * 1.5 + position[0]) * 0.08;
    }
  });

  const progressPct = topic.totalProblems > 0 ? Math.round((topic.solvedCount / topic.totalProblems) * 100) : 0;

  return (
    <group ref={meshRef} position={position}>
      {/* Platform Cylinder */}
      <mesh
        onClick={isUnlocked ? onClick : undefined}
        onPointerOver={() => isUnlocked && setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <cylinderGeometry args={[1.1, 1.25, 0.4, 32]} />
        <meshStandardMaterial
          color={
            isSelected
              ? "#22D3EE"
              : isUnlocked
              ? hovered
                ? "#38BDF8"
                : "#1E293B"
              : "#0F172A"
          }
          emissive={isSelected ? "#22D3EE" : isUnlocked ? "#0369A1" : "#000000"}
          emissiveIntensity={isSelected ? 0.7 : isUnlocked ? 0.25 : 0}
          roughness={0.2}
          metalness={0.7}
        />
      </mesh>

      {/* Glowing ring */}
      {isUnlocked && (
        <mesh position={[0, 0.21, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <ringGeometry args={[0.95, 1.05, 32]} />
          <meshBasicMaterial
            color={isCompleted ? "#22C55E" : isSelected ? "#22D3EE" : "#8B5CF6"}
            side={THREE.DoubleSide}
          />
        </mesh>
      )}

      {/* Html 3D label */}
      <Html position={[0, 0.7, 0]} center distanceFactor={10}>
        <div
          onClick={isUnlocked ? onClick : undefined}
          className={`px-3 py-1.5 rounded-xl backdrop-blur-md text-xs font-semibold whitespace-nowrap transition-all select-none shadow-xl cursor-pointer ${
            isSelected
              ? "bg-cyan-500 text-slate-950 ring-2 ring-cyan-300 scale-110 shadow-cyan-500/40"
              : isUnlocked
              ? "bg-[#121C2F]/90 text-slate-100 border border-slate-700 hover:border-cyan-400 hover:scale-105"
              : "bg-slate-900/80 text-slate-500 border border-slate-800"
          }`}
        >
          <div className="flex items-center gap-1.5">
            {!isUnlocked ? (
              <Lock className="w-3.5 h-3.5 text-slate-500" />
            ) : isCompleted ? (
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
            ) : null}
            <span>{topic.name}</span>
            <span
              className={`text-[10px] px-1.5 py-0.2 rounded-full ${
                isSelected ? "bg-slate-900 text-cyan-300" : "bg-slate-800 text-slate-400"
              }`}
            >
              {progressPct}%
            </span>
          </div>
        </div>
      </Html>
    </group>
  );
}

export default function Roadmap3D({
  topics,
  onSelectTopic,
  selectedTopicSlug,
}: Roadmap3DProps) {
  const [hasWebGL, setHasWebGL] = useState(true);

  useEffect(() => {
    try {
      const c = document.createElement("canvas");
      setHasWebGL(Boolean(c.getContext("webgl") || c.getContext("experimental-webgl")));
    } catch {
      setHasWebGL(false);
    }
  }, []);

  // Compute unlock rules: topic unlocks if prior topic has >= 80% solve rate
  const computedTopics = topics.map((t, idx) => {
    let unlocked = idx === 0;
    if (idx > 0) {
      const prev = topics[idx - 1];
      const prevPct = prev.totalProblems > 0 ? prev.solvedCount / prev.totalProblems : 0;
      unlocked = prevPct >= 0.8 || prev.solvedCount >= 1; // Generous unlocking for MVP
    }
    const completed = t.totalProblems > 0 && t.solvedCount === t.totalProblems;
    return { ...t, isUnlocked: unlocked, isCompleted: completed };
  });

  return (
    <div className="w-full flex flex-col gap-6">
      {/* 3D Visualizer Canvas (or flat fallback) */}
      <div className="relative w-full h-[460px] bg-[#0B1220] rounded-2xl border border-slate-800 overflow-hidden shadow-2xl">
        <div className="absolute top-4 left-4 z-10 bg-[#121C2F]/80 backdrop-blur-md px-3 py-1.5 rounded-lg border border-slate-700/60 text-xs text-slate-300 flex items-center gap-2">
          <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
          <span>Interactive 3D Curriculum &bull; Orbit with drag</span>
        </div>

        {hasWebGL ? (
          <Canvas
            camera={{ position: [0, 4.5, 9.5], fov: 42 }}
            dpr={[1, 1.5]}
            gl={{ antialias: true }}
          >
            <ambientLight intensity={0.7} />
            <pointLight position={[5, 10, 5]} intensity={1.5} color="#22D3EE" />
            <pointLight position={[-5, 5, -5]} intensity={1} color="#8B5CF6" />

            {computedTopics.map((topic, i) => {
              // Spiral layout in 3D
              const angle = (i / computedTopics.length) * Math.PI * 1.5 - 0.7;
              const radius = 4.2;
              const x = Math.sin(angle) * radius;
              const z = -Math.cos(angle) * (radius * 0.7);
              const y = (i - computedTopics.length / 2) * 0.35;

              return (
                <IslandMesh
                  key={topic.id || topic.slug}
                  topic={topic}
                  position={[x, y, z]}
                  isUnlocked={topic.isUnlocked}
                  isCompleted={topic.isCompleted}
                  isSelected={selectedTopicSlug === topic.slug}
                  onClick={() => onSelectTopic(topic)}
                />
              );
            })}

            <OrbitControls
              enablePan={true}
              maxPolarAngle={Math.PI / 2.1}
              minPolarAngle={Math.PI / 6}
            />
          </Canvas>
        ) : (
          <div className="w-full h-full flex items-center justify-center text-slate-400">
            WebGL is unavailable. Use the accessible topic list below.
          </div>
        )}
      </div>

      {/* Accessible Flat SVG / Keyboard Navigation List (Section 4.6 & C1.7) */}
      <div className="bg-[#121C2F] rounded-2xl border border-slate-800 p-5">
        <h2 className="text-sm font-bold uppercase tracking-wider text-slate-400 mb-4 flex items-center gap-2">
          <span>Accessible Topic Progression</span>
          <span className="text-xs lowercase text-slate-500">(Keyboard Navigable)</span>
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
          {computedTopics.map((topic) => {
            const isSelected = selectedTopicSlug === topic.slug;
            return (
              <button
                key={topic.slug}
                disabled={!topic.isUnlocked}
                onClick={() => onSelectTopic(topic)}
                className={`p-3.5 rounded-xl border text-left flex items-center justify-between transition-all focus:outline-none focus:ring-2 focus:ring-cyan-400 ${
                  isSelected
                    ? "bg-cyan-500/10 border-cyan-400 text-cyan-300 shadow-md shadow-cyan-500/10"
                    : topic.isUnlocked
                    ? "bg-[#0B1220] border-slate-800 hover:border-slate-700 text-slate-200"
                    : "bg-[#0B1220]/50 border-slate-850 text-slate-600 cursor-not-allowed opacity-60"
                }`}
              >
                <div>
                  <div className="flex items-center gap-2">
                    {!topic.isUnlocked ? (
                      <Lock className="w-3.5 h-3.5 text-slate-600" />
                    ) : (
                      <span className="w-2 h-2 rounded-full bg-cyan-400" />
                    )}
                    <span className="font-semibold text-sm">{topic.name}</span>
                  </div>
                  <div className="text-xs text-slate-400 mt-1">
                    {topic.solvedCount} / {topic.totalProblems} Solved
                  </div>
                </div>
                <ChevronRight className="w-4 h-4 text-slate-500" />
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
