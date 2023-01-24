import {Header} from '../layout/Header';
import {Content} from '../layout/Content';
import {
  ProjectsProvider,
  SelectedProjectProvider,
  useAuthorizationContext} from "../context";
import {Navigate} from "react-router-dom";

export const TodoistPage = () => {
  const {userCredentials} = useAuthorizationContext();

  if (!userCredentials)
    return <Navigate to={'/login'}/>;

  return (
    <ProjectsProvider>
      <SelectedProjectProvider>
        <main data-testid="application">
          <Header/>
          <Content />
        </main>
      </SelectedProjectProvider>
    </ProjectsProvider>
  );
};
