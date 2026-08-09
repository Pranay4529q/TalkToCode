import client from "./client";

export async function listRepos() {
  const { data } = await client.get("/repos");
  return data;
}

export async function ingestRepo(gitUrl) {
  const { data } = await client.post("/repos/ingest", { git_url: gitUrl });
  return data;
}

export async function getRepoStatus(repoId) {
  const { data } = await client.get(`/repos/${repoId}/status`);
  return data;
}

export async function deleteRepo(repoId) {
  await client.delete(`/repos/${repoId}`);
}
