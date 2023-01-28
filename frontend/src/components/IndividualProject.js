import React, { useState } from 'react';
import { FaTrashAlt } from 'react-icons/fa';
import {useAuthorizationContext, useProjectsValue, useSelectedProjectValue} from '../context';
import {TodoistApi} from "../api/TodoistApi";

export const IndividualProject = ({ project }) => {
  const [showConfirm, setShowConfirm] = useState(false);
  const { projects, setProjects } = useProjectsValue();
  const { setSelectedProject } = useSelectedProjectValue();
  const { token } = useAuthorizationContext();

  const deleteProject = (project_id) => {
    TodoistApi.removeProject(project_id, token).then(() => {
      setProjects([...projects.filter((item) => {return item.id !== project_id;})]);
      setSelectedProject('INBOX');
    })
  };

  return (
    <>
      <span className="sidebar__dot">•</span>
      <span className="sidebar__project-name">{project.title}</span>
      <span
        className="sidebar__project-delete"
        data-testid="delete-project"
        onClick={() => setShowConfirm(!showConfirm)}
        onKeyDown={(e) => {
          if (e.key === 'Enter') setShowConfirm(!showConfirm);
        }}
        tabIndex={0}
        role="button"
        aria-label="Confirm deletion of project"
      >
        <FaTrashAlt />
        {showConfirm && (
          <div className="project-delete-modal">
            <div className="project-delete-modal__inner">
              <p>Are you sure you want to delete this project?</p>
              <button
                type="button"
                onClick={() => deleteProject(project.id)}
              >
                Delete
              </button>
              <span
                onClick={() => setShowConfirm(!showConfirm)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') setShowConfirm(!showConfirm);
                }}
                tabIndex={0}
                role="button"
                aria-label="Cancel adding project, do not delete"
              >
                Cancel
              </span>
            </div>
          </div>
        )}
      </span>
    </>
  );
};