import * as React from "react";
import { Slider as RadixSlider } from "@radix-ui/react-slider";
import { cn } from "/Users/aryanmishra/Verita_AI/dashboard/src/lib/utils.ts";

const Slider = React.forwardRef<
  HTMLDivElement,
  React.ComponentPropsWithoutRef<typeof RadixSlider>
>(({ className, ...props }, ref) => (
  <RadixSlider
    ref={ref}
    className={cn(
      "relative flex w-full touch-none select-none items-center",
      className
    )}
    {...props}
  />
));
Slider.displayName = RadixSlider.displayName;

export { Slider };