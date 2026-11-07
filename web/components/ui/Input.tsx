import React, { forwardRef, InputHTMLAttributes } from "react";

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: React.ReactNode;
  error?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  containerClassName?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      error,
      leftIcon,
      rightIcon,
      className = "",
      containerClassName = "",
      id,
      ...props
    },
    ref
  ) => {
    const inputId = id || (typeof label === "string" ? label.toLowerCase().replace(/\s+/g, "-") : undefined);

    return (
      <div className={`w-full ${containerClassName}`}>
        {label && (
          <label
            htmlFor={inputId}
            className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5"
          >
            {label}
          </label>
        )}
        <div className="relative flex items-center">
          {leftIcon && (
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
              {leftIcon}
            </div>
          )}
          <input
            ref={ref}
            id={inputId}
            className={`w-full rounded-xl border border-slate-700/80 bg-[var(--surface-2,#1A2740)] text-[var(--text-primary,#E2E8F0)] placeholder:text-[var(--text-muted,#94A3B8)] caret-[var(--text-primary,#E2E8F0)] text-sm transition-all focus:outline-none focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/40 focus:ring-offset-1 focus:ring-offset-[#0B1220] disabled:opacity-50 disabled:cursor-not-allowed ${
              leftIcon ? "pl-10" : "px-3.5"
            } ${rightIcon ? "pr-10" : "pr-3.5"} py-2.5 ${
              error ? "border-red-500/80 focus:border-red-400 focus:ring-red-400/30" : ""
            } ${className}`}
            {...props}
          />
          {rightIcon && (
            <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
              {rightIcon}
            </div>
          )}
        </div>
        {error && (
          <p className="mt-1 text-xs text-red-400 animate-in fade-in duration-150">
            {error}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = "Input";

export default Input;
export { Input };
