import type { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "Campus Placement & CS Core | Ready2Code",
  description: "Campus recruitment training for Aptitude, Product DSA, and CS Fundamentals (OS, DBMS, Networks).",
  openGraph: {
    title: "Campus Placement & CS Core | Ready2Code",
    description: "Campus recruitment training for Aptitude, Product DSA, and CS Fundamentals (OS, DBMS, Networks).",
  },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
