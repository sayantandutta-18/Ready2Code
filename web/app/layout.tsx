import "../styles/tokens.css";
import Navbar from "../components/ui/Navbar";
import QueryProvider from "../components/providers/QueryProvider";
import { AuthProvider } from "../lib/authContext";
import AuthModal from "../components/ui/AuthModal";

export const metadata = {
  title: "Ready2Code | 3D Data Structures & Algorithms Arena",
  description: "Next-generation DSA practice platform with 3D algorithm visualizations, pattern-first learning, and competitive arena.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#0B1220] text-[#E2E8F0] antialiased selection:bg-cyan-500/30 selection:text-cyan-200">
        <AuthProvider>
          <QueryProvider>
            <Navbar />
            <AuthModal />
            <main className="min-h-[calc(100vh-65px)]">
              {children}
            </main>
          </QueryProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
