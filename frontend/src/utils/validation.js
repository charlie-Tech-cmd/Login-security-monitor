export const PASSWORD_REQUIREMENTS = [
  {
    id: "length",
    label: "Between 8 and 128 characters",
    test: (password) => password.length >= 8 && password.length <= 128,
  },
  {
    id: "uppercase",
    label: "One uppercase letter (A–Z)",
    test: (password) => /[A-Z]/.test(password),
  },
  {
    id: "lowercase",
    label: "One lowercase letter (a–z)",
    test: (password) => /[a-z]/.test(password),
  },
  {
    id: "number",
    label: "One number (0–9)",
    test: (password) => /[0-9]/.test(password),
  },
  {
    id: "special",
    label: "One special character",
    test: (password) => /[^A-Za-z0-9]/.test(password),
  },
];

export function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
}

export function getPasswordStatus(password) {
  const requirements = PASSWORD_REQUIREMENTS.map((requirement) => ({
    ...requirement,
    met: requirement.test(password),
  }));
  return {
    requirements,
    metCount: requirements.filter((requirement) => requirement.met).length,
    isValid: requirements.every((requirement) => requirement.met),
  };
}
