import type { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "Mock Technical Interview Simulator | Ready2Code",
  description: "Simulated technical interview environment with 20/45 minute timer and blind mode option.",
  openGraph: {
    title: "Mock Technical Interview Simulator | Ready2Code",
    description: "Simulated technical interview environment with 20/45 minute timer and blind mode option.",
  },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
