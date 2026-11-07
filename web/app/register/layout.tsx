import type { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "Create Account | Ready2Code",
  description: "Join Ready2Code to master data structures and algorithms in 3D, build streaks, and prepare for placement tests.",
  openGraph: {
    title: "Create Account | Ready2Code",
    description: "Join Ready2Code to master data structures and algorithms in 3D, build streaks, and prepare for placement tests.",
  },
};

export default function RegisterLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
