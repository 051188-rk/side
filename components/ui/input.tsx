import { cn } from "@/lib/utils"
import { InputHTMLAttributes, forwardRef } from "react"

export const Input = forwardRef<HTMLInputElement, InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => {
    return (
      <input
        ref={ref}
        className={cn(
          "input-field bg-surface-1 text-ink font-body rounded-md px-[14px] py-[10px] border border-hairline focus:outline-none focus:border-accent-blue w-full",
          className
        )}
        {...props}
      />
    )
  }
)

Input.displayName = "Input"
