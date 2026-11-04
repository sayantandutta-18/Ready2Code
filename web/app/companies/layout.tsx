import type { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "Company Interview Roadmaps | Ready2Code",
  description: "Company-specific coding interview questions from Google, Meta, Amazon, Microsoft, and Apple.",
  openGraph: {
    title: "Company Interview Roadmaps | Ready2Code",
    description: "Company-specific coding interview questions from Google, Meta, Amazon, Microsoft, and Apple.",
  },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
