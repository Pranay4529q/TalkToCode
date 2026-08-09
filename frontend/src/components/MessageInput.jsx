import { useState } from "react";

export default function MessageInput({ onSend, disabled }) {
  const [value, setValue] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      handleSubmit(e);
    }
  }

  return (
    <form className="message-input" onSubmit={handleSubmit}>
      <textarea
        className="input mono"
        placeholder="Ask about a function, file, or pattern in this repo…"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        rows={1}
        disabled={disabled}
      />
      <button className="btn" type="submit" disabled={disabled || !value.trim()}>
        Send
      </button>
    </form>
  );
}
