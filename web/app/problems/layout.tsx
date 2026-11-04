import type { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "Problem Arena | Ready2Code",
  description: "Explore 60+ original algorithmic challenges with server-side filtering, Judge0 execution, and live verdicts.",
  openGraph: {
    title: "Problem Arena | Ready2Code",
    description: "Explore 60+ original algorithmic challenges with server-side filtering, Judge0 execution, and live verdicts.",
  },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
