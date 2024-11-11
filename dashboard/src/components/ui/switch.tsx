import * as React from "react";
import { Switch as RadixSwitch } from "@radix-ui/react-switch";
import { cn } from "/Users/aryanmishra/Verita_AI/dashboard/src/lib/utils.ts";

const Switch = React.forwardRef<
  HTMLButtonElement,
  React.ComponentPropsWithoutRef<typeof RadixSwitch>
>(({ className, ...props }, ref) => (
  <RadixSwitch
    ref={ref}
    className={cn(
      "relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2",
      className
    )}
    {...props}
  />
));
Switch.displayName = RadixSwitch.displayName;

export { Switch };