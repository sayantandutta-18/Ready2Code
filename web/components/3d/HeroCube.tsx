"use client";

import React, { useRef, useState, useEffect } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Float, OrbitControls, MeshTransmissionMaterial } from "@react-three/drei";
import * as THREE from "three";

function RotatingCubeMesh({ onFaceClick }: { onFaceClick?: () => void }) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);

  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta * 0.35;
      meshRef.current.rotation.y += delta * 0.45;
      if (hovered) {
        meshRef.current.rotation.z += delta * 0.2;
      }
    }
  });

  return (
    <Float speed={2} rotationIntensity={1.2} floatIntensity={1.5}>
      <mesh
        ref={meshRef}
        scale={hovered ? 1.9 : 1.75}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
        onClick={onFaceClick}
      >
        <boxGeometry args={[1.5, 1.5, 1.5]} />
        <MeshTransmissionMaterial
          backside
          samples={8}
          thickness={0.5}
          roughness={0.12}
          chromaticAberration={0.4}
          anisotropy={0.25}
          distortion={0.3}
          distortionScale={0.4}
          temporalDistortion={0.1}
          color="#22D3EE"
        />
      </mesh>
      {/* Inner glowing core */}
      <mesh scale={0.7}>
        <octahedronGeometry args={[1, 0]} />
        <meshStandardMaterial
          color="#8B5CF6"
          emissive="#8B5CF6"
          emissiveIntensity={1.8}
          wireframe
        />
      </mesh>
    </Float>
  );
}

function StarParticles() {
  const pointsRef = useRef<THREE.Points>(null);
  const count = 75;

  const positions = React.useMemo(() => {
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 8;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 8;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 8;
    }
    return pos;
  }, []);

  useFrame((_, delta) => {
    if (pointsRef.current) {
      pointsRef.current.rotation.y -= delta * 0.08;
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
      <pointsMaterial size={0.045} color="#22D3EE" transparent opacity={0.6} />
    </points>
  );
}

export default function HeroCube({ onFaceClick }: { onFaceClick?: () => void }) {
  const [hasWebGL, setHasWebGL] = useState<boolean>(true);
  const [prefersReducedMotion, setPrefersReducedMotion] = useState<boolean>(false);

  useEffect(() => {
    // Check prefers-reduced-motion
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    setPrefersReducedMotion(mediaQuery.matches);

    // Check WebGL availability
    try {
      const canvas = document.createElement("canvas");
      const gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl");
      setHasWebGL(Boolean(gl));
    } catch {
      setHasWebGL(false);
    }
  }, []);

  // Accessible flat SVG cube fallback (Section 4.6 requirement)
  if (!hasWebGL || prefersReducedMotion) {
    return (
      <div
        className="w-full h-[360px] flex items-center justify-center cursor-pointer group"
        onClick={onFaceClick}
        title="Interactive Ready2Code Isometric Cube"
      >
        <svg
          viewBox="0 0 200 200"
          className="w-56 h-56 transition-transform group-hover:scale-105 duration-300 drop-shadow-[0_0_24px_rgba(34,211,238,0.4)]"
        >
          {/* Top Face */}
          <polygon
            points="100,20 170,60 100,100 30,60"
            fill="url(#topGrad)"
            stroke="#22D3EE"
            strokeWidth="2"
          />
          {/* Left Face */}
          <polygon
            points="30,60 100,100 100,180 30,140"
            fill="url(#leftGrad)"
            stroke="#22D3EE"
            strokeWidth="2"
          />
          {/* Right Face */}
          <polygon
            points="100,100 170,60 170,140 100,180"
            fill="url(#rightGrad)"
            stroke="#8B5CF6"
            strokeWidth="2"
          />
          <defs>
            <linearGradient id="topGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#22D3EE" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#0B1220" stopOpacity="0.9" />
            </linearGradient>
            <linearGradient id="leftGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#0B1220" stopOpacity="0.9" />
              <stop offset="100%" stopColor="#1E293B" stopOpacity="0.9" />
            </linearGradient>
            <linearGradient id="rightGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#8B5CF6" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#121C2F" stopOpacity="0.9" />
            </linearGradient>
          </defs>
        </svg>
      </div>
    );
  }

  return (
    <div className="w-full h-[360px] sm:h-[420px] relative select-none">
      <Canvas
        camera={{ position: [0, 0, 4.2], fov: 45 }}
        dpr={[1, 1.5]}
        gl={{ antialias: true, alpha: true }}
      >
        <ambientLight intensity={0.8} />
        <pointLight position={[10, 10, 10]} intensity={1.5} color="#22D3EE" />
        <pointLight position={[-10, -10, -10]} intensity={1.2} color="#8B5CF6" />
        <StarParticles />
        <RotatingCubeMesh onFaceClick={onFaceClick} />
        <OrbitControls enableZoom={false} enablePan={false} maxPolarAngle={Math.PI / 1.7} minPolarAngle={Math.PI / 2.5} />
      </Canvas>
    </div>
  );
}
