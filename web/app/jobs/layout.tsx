import type { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "Fast-Track Engineering Jobs | Ready2Code",
  description: "Verified software engineering job listings with direct applications and skill matching.",
  openGraph: {
    title: "Fast-Track Engineering Jobs | Ready2Code",
    description: "Verified software engineering job listings with direct applications and skill matching.",
  },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
