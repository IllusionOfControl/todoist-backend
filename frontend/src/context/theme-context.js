import React, {createContext, useContext, useState} from 'react';

export const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const { darkMode, updateThemeMode } = useState(false);

  const switchThemeMode = () => {
    updateThemeMode(!darkMode);
  }

  const value = {darkMode, switchThemeMode};

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useThemeContext = () => useContext(ThemeContext);
