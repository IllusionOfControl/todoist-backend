import {useState, useEffect} from 'react';
import {collatedTasksExist} from '../helpers';
import {TodoistApi} from "../api/TodoistApi";
import {useAuthorizationContext} from "../context/authorization-context";

export const useTasks = selectedProject => {
  const [tasks, setTasks] = useState([]);
  const {userCredentials, clearCredentials} = useAuthorizationContext();

  useEffect(() => {
    let api_call
    if (collatedTasksExist(selectedProject))
      api_call = TodoistApi.getCollatedTasks
    else api_call = TodoistApi.getProjectTasks;

    api_call(selectedProject, userCredentials.token).then((response) => {
      const recieved_tasks = response.data.tasks;
      if (JSON.stringify(recieved_tasks) !== JSON.stringify(tasks)) {
        setTasks(recieved_tasks);
      }
    }, [tasks]).catch((error) => {
      if (error.response.status === 401) {
        clearCredentials();
      }
    });
  })

  return {tasks};
};

export const useProjects = () => {
  const [projects, setProjects] = useState([]);
  const {userCredentials, clearCredentials} = useAuthorizationContext();

  useEffect(() => {
    TodoistApi.getAllProjects(userCredentials.token).then((response) => {
      const received_projects = response.data.projects;
      if (JSON.stringify(received_projects) !== JSON.stringify(projects)) {
        setProjects(received_projects);
      }
    }).catch((error) => {
      if (error.response.status === 401) {
        clearCredentials();
      }
    });
  }, [projects]);

  return {projects, setProjects};
};
