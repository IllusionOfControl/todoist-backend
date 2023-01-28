export const Checkbox = ({ id, taskDesc, onCheck }) => {
  return (
    <div
      className="checkbox-holder"
      data-testid="checkbox-action"
      onClick={() => onCheck(id)}
      onKeyDown={(e) => {
        if (e.key === 'Enter') onCheck(id);
      }}
      aria-label={`Mark ${taskDesc} as done?`}
      role="button"
      tabIndex={0}
    >
      <span className="checkbox" />
    </div>
  );
};
