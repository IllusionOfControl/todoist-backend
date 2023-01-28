import React, { useEffect } from 'react';
import { Checkbox } from './Checkbox';
import { AddTask } from './AddTask';
import { useTasks } from '../hooks';
import { collatedTasks } from '../constants';
import { getTitle, getCollatedTitle, collatedTasksExist } from '../helpers';
import {useSelectedProjectValue, useProjectsValue, useAuthorizationContext} from '../context';
import {TodoistApi} from "../api/TodoistApi";

export const Tasks = () => {
  const { selectedProject } = useSelectedProjectValue();
  const { projects } = useProjectsValue();
  const { tasks, setTasks } = useTasks(selectedProject);
  const { token } = useAuthorizationContext();

  let projectName = '';

  if (collatedTasksExist(selectedProject) && selectedProject) {
    projectName = getCollatedTitle(collatedTasks, selectedProject).name;
  }

  if (
    projects &&
    projects.length > 0 &&
    selectedProject &&
    !collatedTasksExist(selectedProject)
  ) {
    projectName = getTitle(projects, selectedProject).title;
  }

  useEffect(() => {
    document.title = `${projectName}: Todoist`;
  });

  const handleCheck = (id) => {
    TodoistApi.removeTask(selectedProject, id, token).then(r => {
      if (r.status === 204)
        setTasks(tasks.filter((item) => {return item.id !== id}));
    });
  }

  const handleCreate = (task) => {
    setTasks([...tasks, task]);
  }

  return (
    <div className="tasks" data-testid="tasks">
      <h2 data-testid="project-name">{projectName}</h2>

      <ul className="tasks__list">
        {tasks.map((task) => (
          <li key={`${task.id}`}>
            <Checkbox id={task.id} taskDesc={task.title} onCheck={handleCheck}/>
            <span>{task.title}</span>
          </li>
        ))}
      </ul>

      <AddTask onCreate={handleCreate}/>
    </div>
  );
};
