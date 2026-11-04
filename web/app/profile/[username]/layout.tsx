import type { Metadata } from "next";
import React from "react";

type Props = {
  params: { username: string };
  children: React.ReactNode;
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  return {
    title: `${params.username}'s Developer Profile | Ready2Code`,
    description: `View ${params.username}'s solved problems, algorithm mastery, activity heatmap, and Elo rating on Ready2Code.`,
  };
}

export default function ProfileLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
