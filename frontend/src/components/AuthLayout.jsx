import React from "react";
import { Link } from "react-router-dom";

export default function AuthLayout({ title, subtitle, children }) {
  return (
    <section className="my-auto w-full max-w-[440px]" aria-labelledby="auth-title">
      <Link
        className="mx-auto mb-[26px] flex w-fit items-center gap-2.5 font-sans text-[17px] font-extrabold tracking-[-0.04em] text-[#293b4c] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#315e83] max-sm:mb-5"
        to="/register"
        aria-label="L2E CyberGuard home"
      >
        <span
          className="grid size-9 place-items-center rounded-[11px] bg-[#315e83] text-white shadow-sm"
          aria-hidden="true"
        >
          <svg
            className="size-[23px]"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M12 2.75 20 6v5.55c0 5.05-3.43 8.22-8 9.7-4.57-1.48-8-4.65-8-9.7V6l8-3.25Z"
              stroke="currentColor"
              strokeWidth="1.7"
              strokeLinejoin="round"
            />
            <path
              d="m8.75 11.9 2.15 2.15 4.45-4.5"
              stroke="currentColor"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </span>
        <span>
          <span className="mr-1 text-[#315e83]">L2E</span>
          <span>CyberGuard</span>
        </span>
      </Link>

      <div className="rounded-2xl border border-slate-200 bg-white px-10 pb-[30px] pt-[38px] shadow-[0_16px_44px_rgba(33,48,63,0.07)] max-sm:rounded-[13px] max-sm:px-[22px] max-sm:pb-[25px] max-sm:pt-[30px]">
        <header className="mb-7 text-center">
          <h1
            className="m-0 text-[clamp(24px,5vw,28px)] font-bold leading-tight tracking-[-0.045em] text-[#202a35]"
            id="auth-title"
          >
            {title}
          </h1>
          <p className="mt-[9px] text-sm leading-relaxed text-[#697582]">
            {subtitle}
          </p>
        </header>
        {children}
      </div>

      <p className="mt-[22px] text-center text-xs text-[#8b949d]">
        secure learning for guaranteed earning
      </p>
    </section>
  );
}
