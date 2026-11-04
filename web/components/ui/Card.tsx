import React, { HTMLAttributes, forwardRef } from "react";

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "elevated" | "glass" | "interactive";
  glow?: boolean;
}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ children, className = "", variant = "default", glow = false, ...props }, ref) => {
    const baseStyles = "rounded-2xl transition-all border overflow-hidden";

    const variantStyles = {
      default: "bg-[#121C2F] border-slate-800 shadow-xl",
      elevated: "bg-[#162238] border-slate-700/60 shadow-2xl shadow-black/40",
      glass: "bg-[#121C2F]/80 backdrop-blur-md border-slate-800/80 shadow-2xl",
      interactive:
        "bg-[#121C2F] border-slate-800 hover:border-cyan-500/40 hover:bg-[#162238] hover:shadow-cyan-500/10 cursor-pointer shadow-xl active:scale-[0.99]",
    };

    const glowStyles = glow ? "ring-1 ring-cyan-500/30 shadow-cyan-500/20" : "";

    return (
      <div
        ref={ref}
        className={`${baseStyles} ${variantStyles[variant]} ${glowStyles} ${className}`}
        {...props}
      >
        {children}
      </div>
    );
  }
);
Card.displayName = "Card";

export const CardHeader = ({
  children,
  className = "",
  ...props
}: HTMLAttributes<HTMLDivElement>) => (
  <div className={`p-4 sm:p-5 border-b border-slate-800/80 ${className}`} {...props}>
    {children}
  </div>
);
CardHeader.displayName = "CardHeader";

export const CardContent = ({
  children,
  className = "",
  ...props
}: HTMLAttributes<HTMLDivElement>) => (
  <div className={`p-4 sm:p-5 ${className}`} {...props}>
    {children}
  </div>
);
CardContent.displayName = "CardContent";

export const CardFooter = ({
  children,
  className = "",
  ...props
}: HTMLAttributes<HTMLDivElement>) => (
  <div className={`p-4 sm:p-5 border-t border-slate-800/80 bg-[#0E1726]/40 ${className}`} {...props}>
    {children}
  </div>
);
CardFooter.displayName = "CardFooter";

export default Card;
