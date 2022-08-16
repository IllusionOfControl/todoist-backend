/* eslint-disable no-nested-ternary */
import { useState, useEffect } from 'react';
import { collatedTasksExist } from '../helpers';
import { todoistAPI } from '../api'

export const useTasks = selectedProject => {
  const [tasks, setTasks] = useState([]);
  const [archivedTasks, setArchivedTasks] = useState([]);

  useEffect(() => {
    let api_call
    if (collatedTasksExist(selectedProject))
      api_call = todoistAPI.getCollatedTasks
    else api_call = todoistAPI.getProjectTasks;

    api_call(selectedProject).then((response) => {
      const recived_tasks = response.data.tasks;
      if (JSON.stringify(recived_tasks) !== JSON.stringify(tasks)) {
        setTasks(recived_tasks);
      }

    }
      , [tasks])
  })

  return { tasks, archivedTasks };
};

export const useProjects = () => {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    todoistAPI.getUserProjects().then((response) => {
      const recived_projects = response.data.projects
      if (JSON.stringify(recived_projects) !== JSON.stringify(projects)) {
        setProjects(recived_projects);
      }
    });
  }, [projects]);

  return { projects, setProjects };
};
