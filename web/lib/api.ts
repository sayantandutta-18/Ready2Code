const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

export async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  let url = endpoint;
  if (!url.startsWith("http")) {
    if (API_BASE) {
      const base = API_BASE.replace(/\/$/, "");
      const cleanPath = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
      url = `${base}${cleanPath}`;
    } else {
      // Default to Next.js API routes under /api/...
      const cleanPath = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
      url = cleanPath.startsWith("/api") ? cleanPath : `/api${cleanPath}`;
    }
  }

  // Attach auth token if available in browser
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options?.headers as Record<string, string> || {}),
  };

  if (typeof window !== "undefined") {
    const token = localStorage.getItem("ready2code_auth_token");
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
      headers["X-User-Id"] = token;
    }
  }

  const res = await fetch(url, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const errorBody = await res.text();
    let errorDetail = res.statusText;
    try {
      const parsed = JSON.parse(errorBody);
      errorDetail = parsed.detail || parsed.message || errorDetail;
    } catch {
      if (errorBody) errorDetail = errorBody;
    }
    throw new Error(errorDetail || `API request failed with status ${res.status}`);
  }

  return res.json();
}
