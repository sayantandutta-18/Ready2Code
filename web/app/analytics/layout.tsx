import type { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "Learner Performance Analytics | Ready2Code",
  description: "Track problem solve velocity, topic mastery distributions, and identified algorithmic weak spots.",
  openGraph: {
    title: "Learner Performance Analytics | Ready2Code",
    description: "Track problem solve velocity, topic mastery distributions, and identified algorithmic weak spots.",
  },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
