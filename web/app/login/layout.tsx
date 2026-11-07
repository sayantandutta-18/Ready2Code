import type { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "Sign In | Ready2Code",
  description: "Sign in to your Ready2Code account to track your problem streak, save code drafts, and prepare for placement tests.",
  openGraph: {
    title: "Sign In | Ready2Code",
    description: "Sign in to your Ready2Code account to track your problem streak, save code drafts, and prepare for placement tests.",
  },
};

export default function LoginLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
