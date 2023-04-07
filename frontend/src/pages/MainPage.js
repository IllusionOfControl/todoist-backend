import {Header} from '../components/Header';
import {
  ProjectsProvider,
  SelectedProjectProvider,
  useAuthorizationContext, useThemeContext
} from "../context";
import {Navigate} from "react-router-dom";
import {Sidebar} from "../components/Sidebar";
import {Tasks} from "../components/Tasks";
import React from "react";

export const MainPage = () => {
  const {token} = useAuthorizationContext();
  const {darkMode} = useThemeContext();

  if (!token)
    return <Navigate to={'/login'}/>;

  return (
    <ProjectsProvider>
      <SelectedProjectProvider>
        <main data-testid="application" className={darkMode ? "darkmode" : undefined}>
          <Header/>
          <section className="content">
            <Sidebar />
            <Tasks />
          </section>
        </main>
      </SelectedProjectProvider>
    </ProjectsProvider>
  );
};
