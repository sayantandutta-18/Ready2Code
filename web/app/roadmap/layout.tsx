import type { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "3D Roadmap Curriculum | Ready2Code",
  description: "Interactive 3D topic progression from array foundations to advanced dynamic programming.",
  openGraph: {
    title: "3D Roadmap Curriculum | Ready2Code",
    description: "Interactive 3D topic progression from array foundations to advanced dynamic programming.",
  },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
