import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import SourcesPanel from "./SourcesPanel";

export default function MessageList({ messages, isSending }) {
  if (messages.length === 0) {
    return (
      <div className="empty-chat">
        <p className="empty-chat-title">Ask anything about this codebase</p>
        <p className="empty-chat-sub">
          e.g. "where is the auth token validated?" or "what does the chunker do with classes?"
        </p>
      </div>
    );
  }

  return (
    <div className="message-list">
      {messages.map((m, i) => (
        <div key={i} className={`message message-${m.role}`}>
          <div className="message-role mono">{m.role === "user" ? "you" : "gitchat"}</div>
          <div className="message-body">
            <ReactMarkdown
              components={{
                code({ inline, className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || "");
                  return !inline && match ? (
                    <SyntaxHighlighter style={oneDark} language={match[1]} PreTag="div" {...props}>
                      {String(children).replace(/\n$/, "")}
                    </SyntaxHighlighter>
                  ) : (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  );
                },
              }}
            >
              {m.content}
            </ReactMarkdown>
          </div>
          {m.role === "assistant" && m.sources?.length > 0 && <SourcesPanel sources={m.sources} />}
        </div>
      ))}

      {isSending && (
        <div className="message message-assistant">
          <div className="message-role mono">gitchat</div>
          <div className="message-body pulse mono">searching the codebase…</div>
        </div>
      )}
    </div>
  );
}
