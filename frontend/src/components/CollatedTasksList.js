import { collatedTasks } from '../constants'
import { useSelectedProjectValue } from '../context/selected-project-context'


export const CollatedTasksList = () => {
  const { selectedProject, setSelectedProject } = useSelectedProjectValue();

  const tasks = collatedTasks.map((item) => {
    const Icon = item.icon;
    return (
      <li
        key={item.key}
        data-testid="inbox"
        className={selectedProject === item.key ? 'active' : undefined}
      >
        <div
          data-testid="inbox-action"
          aria-label="Show inbox tasks"
          tabIndex={0}
          role="button"
          onClick={() => {
            setSelectedProject(item.key);
          }}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              setSelectedProject(item.key);
            }
          }}
        >
          <span>
            <Icon/>
          </span>
          <span>{item.name}</span>
        </div>
      </li>
      )})

  return (
    <ul className="sidebar__generic">
      {tasks}
    </ul>
  )
}