import React, { useState } from 'react';
import { FaPizzaSlice, FaSignOutAlt, FaPlus } from 'react-icons/fa';
import { AddTask } from './AddTask';
import {useAuthorizationContext, useThemeContext} from "../context";

export const Header = () => {
  const [shouldShowMain, setShouldShowMain] = useState(false);
  const [showQuickAddTask, setShowQuickAddTask] = useState(false);
  const {switchThemeMode} = useThemeContext();
  const {resetCredentials} = useAuthorizationContext()

  return (
    <header className="header" data-testid="header">
      <nav>
        <div className="logo">
          <img src="/images/logo.png" alt="Todoist" />
        </div>
        <div className="settings">
          <ul>
            <li className="settings__item">
              <button
                data-testid="quick-add-task-action"
                aria-label="Quick add task"
                type="button"
                onClick={() => {
                  setShowQuickAddTask(true);
                  setShouldShowMain(true);
                }}
              >
                <FaPlus />
              </button>
            </li>
            <li className="settings__item">
              <button
                data-testid="dark-mode-action"
                aria-label="Darkmode on/off"
                type="button"
                onClick={switchThemeMode}
              >
                <FaPizzaSlice />
              </button>
            </li>
            <li className="settings__item">
              <button
                data-testid="dark-mode-action"
                aria-label="Darkmode on/off"
                type="button"
                onClick={resetCredentials}
              >
                <FaSignOutAlt />
              </button>
            </li>
          </ul>
        </div>
      </nav>

      <AddTask
        showAddTaskMain={false}
        shouldShowMain={shouldShowMain}
        showQuickAddTask={showQuickAddTask}
        setShowQuickAddTask={setShowQuickAddTask}
      />
    </header>
  );
};
