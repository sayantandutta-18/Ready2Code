const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  // Use relative /api path if client-side and Next rewrites are enabled, or absolute API_BASE
  const url = endpoint.startsWith("http")
    ? endpoint
    : endpoint.startsWith("/api")
    ? endpoint
    : `${API_BASE}${endpoint.startsWith("/") ? "" : "/"}${endpoint}`;

  const res = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
    },
    ...options,
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
