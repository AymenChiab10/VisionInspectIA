// Role : Hook d'acces au theme (light/dark).

import { useContext } from "react";
import { ThemeContext } from "../context/ThemeContext";

export function useTheme() {
  const context = useContext(ThemeContext);

  if (!context) {
    throw new Error("useTheme doit etre utilise a l'interieur d'un ThemeProvider.");
  }

  return context;
}
