import type { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "Curated Study Lists | Ready2Code",
  description: "Structured problem lists including Blind 75 and NeetCode 150 essentials.",
  openGraph: {
    title: "Curated Study Lists | Ready2Code",
    description: "Structured problem lists including Blind 75 and NeetCode 150 essentials.",
  },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
