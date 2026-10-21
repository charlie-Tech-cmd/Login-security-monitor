import React, { useState } from "react";
import { getPasswordStatus } from "../utils/validation.js";

export default function PasswordField({
  id = "password",
  label = "Password",
  value,
  onChange,
  onBlur,
  onFocus,
  error,
  showStrength = false,
  autoComplete = "current-password",
  describedBy,
}) {
  const [visible, setVisible] = useState(false);
  const [focused, setFocused] = useState(false);
  const [touched, setTouched] = useState(false);
  const { requirements, metCount, isValid } = getPasswordStatus(value);
  const requirementsVisible =
    showStrength && (focused || (touched && !isValid));
  const strengthLabel =
    metCount === 0
      ? "Add a password"
      : metCount === 5
        ? "Strong"
        : metCount >= 3
          ? "Almost there"
          : "Weak";
  const strengthId = `${id}-strength`;
  const requirementsId = `${id}-requirements`;
  const errorId = `${id}-error`;
  const ids = [
    describedBy,
    showStrength ? strengthId : null,
    requirementsVisible ? requirementsId : null,
    error ? errorId : null,
  ].filter(Boolean);

  function handleFocus(event) {
    setFocused(true);
    onFocus?.(event);
  }

  function handleBlur(event) {
    setFocused(false);
    setTouched(true);
    onBlur?.(event);
  }

  return (
    <div className="min-w-0">
      <label
        className="mb-2 block text-[13px] font-semibold text-[#34414e]"
        htmlFor={id}
      >
        {label}
      </label>
      <div className="relative">
        <input
          className={`block h-[46px] w-full rounded-lg border bg-white px-[13px] pr-[66px] text-sm text-[#202a35] outline-none transition-colors hover:border-slate-400 focus:border-[#315e83] focus:ring-[3px] focus:ring-[#315e83]/15 ${
            error ? "border-[#bf6666]" : "border-[#cfd6de]"
          }`}
          id={id}
          name={id}
          type={visible ? "text" : "password"}
          value={value}
          onChange={onChange}
          onFocus={handleFocus}
          onBlur={handleBlur}
          autoComplete={
            id === "confirmPassword" ? "new-password" : autoComplete
          }
          aria-invalid={Boolean(error)}
          aria-describedby={ids.length ? ids.join(" ") : undefined}
          required
        />
        <button
          className="absolute right-2 top-1/2 -translate-y-1/2 rounded px-[7px] py-1.5 text-xs font-semibold text-[#526b80] hover:bg-slate-100 hover:text-[#294e6d] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#315e83]"
          type="button"
          aria-label={visible ? "Hide password" : "Show password"}
          aria-pressed={visible}
          onClick={() => setVisible((current) => !current)}
        >
          {visible ? "Hide" : "Show"}
        </button>
      </div>

      {showStrength && (
        <div className="mt-[9px]">
          <div className="flex min-h-[13px] items-center gap-2.5">
            <div
              className="flex flex-1 gap-1"
              id={strengthId}
              role="img"
              aria-label={`${metCount} of 5 password requirements met`}
            >
              {requirements.map((requirement, index) => (
                <span
                  className={`h-1 flex-1 rounded-full transition-colors motion-reduce:transition-none ${
                    index < metCount
                      ? metCount === 5
                        ? "bg-emerald-700"
                        : metCount >= 3
                          ? "bg-amber-600"
                          : "bg-orange-700"
                      : "bg-slate-200"
                  }`}
                  key={requirement.id}
                />
              ))}
            </div>
            <span className="min-w-[76px] text-right text-[11px] text-[#687582]" aria-live="polite">
              {strengthLabel}
            </span>
          </div>

          <div
            className={`grid transition-[grid-template-rows,opacity,margin] duration-200 motion-reduce:transition-none ${
              requirementsVisible
                ? "mt-2.5 grid-rows-[1fr] opacity-100"
                : "grid-rows-[0fr] opacity-0"
            }`}
            id={requirementsId}
            aria-hidden={!requirementsVisible}
          >
            <ul className="m-0 min-h-0 list-none overflow-hidden p-0">
              {requirements.map((requirement) => (
                <li
                  className={`flex items-center gap-2 py-[3px] text-[11.5px] leading-[1.45] ${
                    requirement.met ? "text-[#486652]" : "text-[#6b7681]"
                  }`}
                  key={requirement.id}
                >
                  <span
                    className={`grid size-[14px] flex-none place-items-center rounded-full border text-[9px] font-bold leading-none text-white ${
                      requirement.met
                        ? "border-[#668570] bg-[#668570]"
                        : "border-[#bac3cb]"
                    }`}
                    aria-hidden="true"
                  >
                    {requirement.met ? "✓" : ""}
                  </span>
                  <span>{requirement.label}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {error && (
        <p className="mt-[7px] text-xs leading-[1.4] text-[#a23c3c]" id={errorId}>
          {error}
        </p>
      )}
    </div>
  );
}
