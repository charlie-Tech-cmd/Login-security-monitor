const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ?? ""
).replace(/\/+$/, "");
console.log(API_BASE_URL)
export const AUTH_ENDPOINTS = {
  register: `${API_BASE_URL}/api/auth/register`,
  login: `${API_BASE_URL}/api/auth/login`,
  me: `${API_BASE_URL}/api/auth/me`,
};

const TOKEN_KEY = "access_token";

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request(endpoint, options = {}) {
  const response = await fetch(endpoint, options);

  let data = {};

  try {
    data = await response.json();
  } catch {
    // The server may return an empty or non-JSON response.
  }

  if (!response.ok) {
    let message = `Request failed with status ${response.status}.`;

    if (typeof data.detail === "string") {
      message = data.detail;
    } else if (Array.isArray(data.detail) && data.detail.length > 0) {
      message = data.detail
        .map((item) =>
          typeof item === "object" && item?.msg ? item.msg : String(item),
        )
        .join("; ");
    }

    throw new ApiError(message, response.status);
  }

  return data;
}

export async function register(credentials) {
  return request(AUTH_ENDPOINTS.register, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  });
}

export async function login(credentials) {
  const data = await request(AUTH_ENDPOINTS.login, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  });

  if (!data.access_token) {
    throw new ApiError(
      "The server did not return an authentication token.",
      500,
    );
  }

  sessionStorage.setItem(TOKEN_KEY, data.access_token);

  return data;
}

export function getToken() {
  return sessionStorage.getItem(TOKEN_KEY);
}

export async function getCurrentUser() {
  const token = getToken();

  if (!token) {
    throw new ApiError("You are not signed in.", 401);
  }

  return request(AUTH_ENDPOINTS.me, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export function logout() {
  sessionStorage.removeItem(TOKEN_KEY);
}
