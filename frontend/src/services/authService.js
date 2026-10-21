const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "").replace(
  /\/+$/,
  "",
);

export const AUTH_ENDPOINTS = {
  register: `${API_BASE_URL}/api/auth/register`,
  login: `${API_BASE_URL}/api/auth/login`,
};

async function post(endpoint, credentials) {
  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials),
  });

  return response.ok;
}

export function register(credentials) {
  return post(AUTH_ENDPOINTS.register, credentials);
}

export function login(credentials) {
  return post(AUTH_ENDPOINTS.login, credentials);
}
