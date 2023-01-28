import {SignInPage, SignUpPage, MainPage} from "./pages";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import {useEffect} from "react";
import {useThemeContext} from "./context";

export const App = () => {
  const {darkMode} = useThemeContext();

  useEffect(() => {
    if (darkMode) document.body.classList.add('dark');
    else document.body.classList.remove('dark')
  }, [darkMode]);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainPage/>}/>
        <Route path="/login" element={<SignInPage/>}/>
        <Route path="/registration" element={<SignUpPage/>}/>
      </Routes>
    </BrowserRouter>
  );
};
