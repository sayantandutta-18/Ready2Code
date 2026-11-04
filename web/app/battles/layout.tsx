import type { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "1v1 Live Code Battles | Ready2Code",
  description: "Real-time head-to-head 1v1 competitive coding matches with live execution checks.",
  openGraph: {
    title: "1v1 Live Code Battles | Ready2Code",
    description: "Real-time head-to-head 1v1 competitive coding matches with live execution checks.",
  },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
