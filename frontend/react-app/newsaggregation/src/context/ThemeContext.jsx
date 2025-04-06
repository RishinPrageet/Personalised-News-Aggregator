"use client"

import { createContext, useContext, useEffect, useState } from "react"

const ThemeContext = createContext()

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState(() => {
    // Check if theme is stored in localStorage
    const savedTheme = localStorage.getItem("theme")
    // Check system preference if no saved theme
    if (!savedTheme) {
      return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"
    }
    return savedTheme
  })

  useEffect(() => {
    // Update localStorage when theme changes
    localStorage.setItem("theme", theme)

    // Update document class for CSS
    if (theme === "dark") {
      document.documentElement.classList.add("dark")
    } else {
      document.documentElement.classList.remove("dark")
    }
  }, [theme])

  const toggleTheme = () => {
    setTheme(theme === "light" ? "dark" : "light")
  }

  return <ThemeContext.Provider value={{ theme, toggleTheme }}>{children}</ThemeContext.Provider>
}

export const useTheme = () => useContext(ThemeContext)

