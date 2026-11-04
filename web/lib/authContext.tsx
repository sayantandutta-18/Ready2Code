"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { fetchApi } from "./api";

export interface AuthUser {
  id: string;
  username: string;
  display_name: string;
  avatar_url?: string;
  timezone: string;
  streak: number;
  xp: number;
  solved_count: number;
}

interface AuthContextType {
  user: AuthUser | null;
  token: string | null;
  isLoading: boolean;
  login: (username: string, password?: string) => Promise<void>;
  register: (username: string, displayName?: string, timezone?: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
  isAuthModalOpen: boolean;
  openAuthModal: () => void;
  closeAuthModal: () => void;
  requireAuth: (callback: () => void) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [pendingAction, setPendingAction] = useState<(() => void) | null>(null);

  // Load user from localStorage and verify on mount
  useEffect(() => {
    if (typeof window === "undefined") return;

    const savedToken = localStorage.getItem("ready2code_auth_token");
    const savedUser = localStorage.getItem("ready2code_auth_user");

    if (savedToken && savedUser) {
      try {
        setToken(savedToken);
        setUser(JSON.parse(savedUser));
      } catch {
        localStorage.removeItem("ready2code_auth_token");
        localStorage.removeItem("ready2code_auth_user");
      }
    }
    setIsLoading(false);

    // Fetch latest user data in background if logged in
    if (savedToken) {
      fetchApi<AuthUser>("/auth/me")
        .then((latestUser) => {
          setUser(latestUser);
          localStorage.setItem("ready2code_auth_user", JSON.stringify(latestUser));
        })
        .catch(() => {
          // Token expired or invalid
        });
    }
  }, []);

  const login = async (username: string, password?: string) => {
    const res = await fetchApi<{ token: string; user: AuthUser }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    });

    setToken(res.token);
    setUser(res.user);
    localStorage.setItem("ready2code_auth_token", res.token);
    localStorage.setItem("ready2code_auth_user", JSON.stringify(res.user));
    setIsAuthModalOpen(false);

    if (pendingAction) {
      pendingAction();
      setPendingAction(null);
    }
  };

  const register = async (username: string, displayName?: string, timezone?: string) => {
    const tz = timezone || Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC";
    const res = await fetchApi<{ token: string; user: AuthUser }>("/auth/register", {
      method: "POST",
      body: JSON.stringify({ username, display_name: displayName, timezone: tz }),
    });

    setToken(res.token);
    setUser(res.user);
    localStorage.setItem("ready2code_auth_token", res.token);
    localStorage.setItem("ready2code_auth_user", JSON.stringify(res.user));
    setIsAuthModalOpen(false);

    if (pendingAction) {
      pendingAction();
      setPendingAction(null);
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("ready2code_auth_token");
    localStorage.removeItem("ready2code_auth_user");
  };

  const refreshUser = async () => {
    if (!token) return;
    try {
      const latestUser = await fetchApi<AuthUser>("/auth/me");
      setUser(latestUser);
      localStorage.setItem("ready2code_auth_user", JSON.stringify(latestUser));
    } catch {
      // Ignore background refresh errors
    }
  };

  const openAuthModal = () => setIsAuthModalOpen(true);
  const closeAuthModal = () => {
    setIsAuthModalOpen(false);
    setPendingAction(null);
  };

  const requireAuth = (callback: () => void) => {
    if (user) {
      callback();
    } else {
      setPendingAction(() => callback);
      setIsAuthModalOpen(true);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        login,
        register,
        logout,
        refreshUser,
        isAuthModalOpen,
        openAuthModal,
        closeAuthModal,
        requireAuth,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
