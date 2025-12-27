export interface SyntaxExample {
  id: string;
  title: string;
  description: string;
  code: string;
  category: SyntaxCategory;
}

export type SyntaxCategory = 
  | "workflow"
  | "action"
  | "logic"
  | "state"
  | "component"
  | "variable";

import type { LucideIcon } from "lucide-react";

export interface CategoryInfo {
  name: string;
  description: string;
  Icon: LucideIcon;
}
