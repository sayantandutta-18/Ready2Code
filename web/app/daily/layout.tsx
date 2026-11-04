import type { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "Daily Challenge & Streak | Ready2Code",
  description: "Solve the daily algorithmic challenge to maintain your streak in your local timezone.",
  openGraph: {
    title: "Daily Challenge & Streak | Ready2Code",
    description: "Solve the daily algorithmic challenge to maintain your streak in your local timezone.",
  },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
