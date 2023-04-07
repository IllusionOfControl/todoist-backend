import {useState, useEffect} from 'react';
import {collatedTasksExist} from '../helpers';
import {TodoistApi} from "../api/TodoistApi";
import {useAuthorizationContext} from "../context";

export const useTasks = project => {
  const [tasks, setTasks] = useState([]);
  const {token, resetCredentials} = useAuthorizationContext();

  useEffect(() => {
    let apiCall
    if (collatedTasksExist(project))
      apiCall = TodoistApi.getCollatedTasks
    else apiCall = TodoistApi.getProjectTasks;

    apiCall(project, token).then((response) => {
      const recievedTasks = response.data.tasks;
      if (JSON.stringify(recievedTasks) !== JSON.stringify(tasks)) {
        setTasks(recievedTasks);
      }
    }, [tasks]).catch((error) => {
      if (error.response.status === 403) {
        resetCredentials();
      }
    });
  }, [resetCredentials, project, token])

  return {tasks, setTasks};
};

export const useProjects = () => {
  const [projects, setProjects] = useState([]);
  const {token, resetCredentials} = useAuthorizationContext();

  useEffect(() => {
    TodoistApi.getAllProjects(token).then((response) => {
      const received_projects = response.data.projects;
      if (JSON.stringify(received_projects) !== JSON.stringify(projects)) {
        setProjects(received_projects);
      }
    }).catch((error) => {
      if (error.response.status === 403) {
        resetCredentials();
      }
    });
  }, [resetCredentials, token]);

  return {projects, setProjects};
};

export const useInput = (initialValue, validatorCallback = f => f) => {
  const [value, setValue] = useState(initialValue);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const inputValue = e.target.value;
    setValue(inputValue);
    setError(validatorCallback(inputValue));
  };

  return [value, handleChange, error];
};
