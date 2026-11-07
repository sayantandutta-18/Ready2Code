"use client";

import React, { useRef, useState, useEffect, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Float, OrbitControls, MeshTransmissionMaterial } from "@react-three/drei";
import * as THREE from "three";

interface AuthSpatialProps {
  variant?: "login" | "register";
  className?: string;
}

// Interactive Central Holographic Core
function HologramVaultCore({ variant = "login" }: { variant?: "login" | "register" }) {
  const coreRef = useRef<THREE.Group>(null);
  const ringRef1 = useRef<THREE.Mesh>(null);
  const ringRef2 = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);

  const isLogin = variant === "login";
  const primaryColor = isLogin ? "#22D3EE" : "#10B981";
  const secondaryColor = isLogin ? "#8B5CF6" : "#06B6D4";

  useFrame((state, delta) => {
    if (coreRef.current) {
      coreRef.current.rotation.y += delta * (hovered ? 0.7 : 0.4);
      coreRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.8) * 0.15;
    }
    if (ringRef1.current) {
      ringRef1.current.rotation.z += delta * 0.5;
      ringRef1.current.rotation.x += delta * 0.2;
    }
    if (ringRef2.current) {
      ringRef2.current.rotation.z -= delta * 0.35;
      ringRef2.current.rotation.y += delta * 0.25;
    }
  });

  return (
    <Float speed={2.5} rotationIntensity={1.2} floatIntensity={1.8}>
      <group
        ref={coreRef}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        {/* Main Central Geometric Crystal */}
        <mesh scale={hovered ? 1.4 : 1.25}>
          {isLogin ? (
            <octahedronGeometry args={[1, 0]} />
          ) : (
            <dodecahedronGeometry args={[1, 0]} />
          )}
          <MeshTransmissionMaterial
            backside
            samples={6}
            thickness={0.6}
            roughness={0.15}
            chromaticAberration={0.4}
            anisotropy={0.2}
            distortion={0.25}
            distortionScale={0.3}
            color={primaryColor}
          />
        </mesh>

        {/* Inner Pulsing Wireframe Core */}
        <mesh scale={0.7}>
          <icosahedronGeometry args={[0.9, 0]} />
          <meshStandardMaterial
            color={secondaryColor}
            emissive={secondaryColor}
            emissiveIntensity={hovered ? 2.8 : 1.9}
            wireframe
          />
        </mesh>

        {/* Outer Orbital Ring 1 */}
        <mesh ref={ringRef1} scale={2.2}>
          <torusGeometry args={[1, 0.02, 16, 64]} />
          <meshStandardMaterial
            color={primaryColor}
            emissive={primaryColor}
            emissiveIntensity={1.2}
            transparent
            opacity={0.7}
          />
        </mesh>

        {/* Outer Orbital Ring 2 (Tilted) */}
        <mesh ref={ringRef2} scale={2.5} rotation={[Math.PI / 3, Math.PI / 4, 0]}>
          <torusGeometry args={[1, 0.015, 16, 64]} />
          <meshStandardMaterial
            color={secondaryColor}
            emissive={secondaryColor}
            emissiveIntensity={1.4}
            transparent
            opacity={0.5}
          />
        </mesh>

        {/* Orbiting Satellite Data Nodes */}
        {[-1.8, 1.8].map((x, idx) => (
          <mesh key={idx} position={[x, (idx - 0.5) * 1.2, (idx - 0.5) * 0.8]} scale={0.18}>
            <sphereGeometry args={[1, 16, 16]} />
            <meshStandardMaterial
              color={idx === 0 ? "#F59E0B" : "#EC4899"}
              emissive={idx === 0 ? "#F59E0B" : "#EC4899"}
              emissiveIntensity={2.2}
            />
          </mesh>
        ))}
      </group>
    </Float>
  );
}

// Swirling Spatial Star & Code Dust Particles
function AuthCosmicDust({ count = 90, color = "#22D3EE" }: { count?: number; color?: string }) {
  const pointsRef = useRef<THREE.Points>(null);

  const positions = useMemo(() => {
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 9;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 9;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 9;
    }
    return pos;
  }, [count]);

  useFrame((_, delta) => {
    if (pointsRef.current) {
      pointsRef.current.rotation.y -= delta * 0.06;
      pointsRef.current.rotation.x += delta * 0.03;
    }
  });

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          itemSize={3}
          array={positions}
        />
      </bufferGeometry>
      <pointsMaterial size={0.05} color={color} transparent opacity={0.65} />
    </points>
  );
}

export default function AuthSpatialCanvas({
  variant = "login",
  className = "w-full h-[320px] lg:h-[460px]",
}: AuthSpatialProps) {
  const [hasWebGL, setHasWebGL] = useState<boolean>(true);
  const [prefersReducedMotion, setPrefersReducedMotion] = useState<boolean>(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    setPrefersReducedMotion(mediaQuery.matches);

    try {
      const canvas = document.createElement("canvas");
      const gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl");
      setHasWebGL(Boolean(gl));
    } catch {
      setHasWebGL(false);
    }
  }, []);

  // Accessible 2D Fallback
  if (!hasWebGL || prefersReducedMotion) {
    return (
      <div
        className={`${className} flex flex-col items-center justify-center p-6 bg-[#070D18]/80 border border-cyan-500/20 rounded-2xl relative overflow-hidden`}
      >
        <div className="w-24 h-24 rounded-2xl bg-gradient-to-tr from-cyan-500/20 to-violet-500/20 border border-cyan-500/40 flex items-center justify-center shadow-lg shadow-cyan-500/10">
          <div className="w-12 h-12 rounded-xl border-2 border-dashed border-cyan-400 flex items-center justify-center animate-spin" style={{ animationDuration: "10s" }}>
            <span className="text-cyan-300 font-mono text-sm font-bold">3D</span>
          </div>
        </div>
        <p className="text-xs text-slate-400 font-mono mt-4 text-center">
          {variant === "login" ? "Holographic Key Vault" : "Algorithmic Genesis Matrix"}
        </p>
      </div>
    );
  }

  const dustColor = variant === "login" ? "#22D3EE" : "#10B981";

  return (
    <div className={`relative ${className} select-none`}>
      {/* Background ambient glow */}
      <div className="absolute inset-0 bg-radial-gradient from-cyan-500/10 via-transparent to-transparent pointer-events-none blur-2xl" />

      <Canvas
        camera={{ position: [0, 0, 5], fov: 45 }}
        gl={{ antialias: true, alpha: true, powerPreference: "high-performance" }}
        className="w-full h-full cursor-grab active:cursor-grabbing"
      >
        <ambientLight intensity={0.7} />
        <directionalLight position={[10, 10, 5]} intensity={1.5} color="#FFFFFF" />
        <pointLight position={[-10, -10, -5]} intensity={2.0} color="#8B5CF6" />
        <pointLight position={[0, 5, -3]} intensity={1.5} color="#22D3EE" />

        <HologramVaultCore variant={variant} />
        <AuthCosmicDust count={80} color={dustColor} />

        <OrbitControls
          enableZoom={false}
          enablePan={false}
          maxPolarAngle={Math.PI / 1.7}
          minPolarAngle={Math.PI / 2.3}
          rotateSpeed={0.5}
        />
      </Canvas>

      {/* Floating 3D HUD Badge */}
      <div className="absolute bottom-3 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full bg-slate-900/80 border border-cyan-500/30 backdrop-blur-md text-[10px] text-cyan-300 font-mono flex items-center gap-1.5 shadow-md pointer-events-none">
        <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse" />
        <span>3D Spatial Hologram &bull; Drag to Rotate</span>
      </div>
    </div>
  );
}
