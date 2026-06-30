import { cn } from "@/lib/utils"
import { ButtonHTMLAttributes, forwardRef } from "react"

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "tertiary"
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "text-sm font-medium px-5 py-2.5 transition-all rounded-lg hover:shadow-md active:scale-95",
          {
            "bg-white text-black hover:opacity-80": variant === "primary",
            "bg-surface text-text-primary border border-border hover:bg-white/10": variant === "secondary",
            "bg-transparent text-white border border-white hover:bg-white/10": variant === "tertiary",
          },
          className
        )}
        {...props}
      />
    )
  }
)

Button.displayName = "Button"
