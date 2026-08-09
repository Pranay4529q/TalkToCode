const LABELS = {
  ready: "ready",
  processing: "indexing",
  failed: "failed",
};

export default function StatusBadge({ status }) {
  return <span className={`status-pill status-${status}`}>{LABELS[status] || status}</span>;
}
