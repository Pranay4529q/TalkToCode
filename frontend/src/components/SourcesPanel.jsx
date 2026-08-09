export default function SourcesPanel({ sources }) {
  return (
    <div className="sources-panel">
      <span className="sources-label">sources</span>
      <div className="sources-chips">
        {sources.map((s, i) => (
          <span key={i} className="source-chip mono" title={`${s.chunk_type} · score ${s.score.toFixed(2)}`}>
            {s.file_path}
            <span className="source-chip-lines">
              :{s.start_line}-{s.end_line}
            </span>
          </span>
        ))}
      </div>
    </div>
  );
}
