/* El navegador habla con la API; nunca se conecta directamente a la BD. */
const $ = (selector) => document.querySelector(selector);
let csrf = "", projects = [], experiments = [], selectedId = null;
let editingProject = null, editingExperiment = null, noticeTimer;

function notify(message) {
  $("#notice").textContent = message;
  $("#notice").hidden = false;
  clearTimeout(noticeTimer);
  noticeTimer = setTimeout(() => { $("#notice").hidden = true; }, 6000);
}

function showLogin() {
  document.querySelectorAll("dialog[open]").forEach((dialog) => dialog.close());
  $("#workspace").hidden = true;
  $("#login-view").hidden = false;
  csrf = "";
}

async function api(path, options = {}) {
  const response = await fetch(`/api${path}`, {
    credentials: "same-origin",
    ...options,
    headers: { "Content-Type": "application/json", "X-CSRF-Token": csrf, ...options.headers },
  });
  if (response.status === 204) return null;
  const body = await response.json();
  if (!response.ok) {
    if (response.status === 401 && path !== "/auth/login") showLogin();
    const message = Array.isArray(body.detail)
      ? body.detail.map((item) => `${item.loc.slice(1).join(".")}: ${item.msg}`).join("; ")
      : body.detail;
    const error = new Error(message || "No se pudo completar la operación.");
    error.status = response.status;
    throw error;
  }
  return body;
}

function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}

async function enterWorkspace(user) {
  csrf = user.csrf_token;
  $("#user-email").textContent = user.email;
  $("#login-view").hidden = true;
  $("#workspace").hidden = false;
  selectedId = null;
  await refresh();
}

async function refresh() {
  $("#project-list").textContent = "Cargando proyectos…";
  const [list, summary] = await Promise.all([
    api("/projects").catch((error) => { if (error.status === 501) return null; throw error; }),
    api("/summary"),
  ]);
  projects = list || [];
  $("#project-count").textContent = summary.projects;
  $("#experiment-count").textContent = summary.experiments;
  if (!projects.some((project) => project.id === selectedId)) selectedId = projects[0]?.id ?? null;
  renderProjects();
  if (list === null) $("#project-list").replaceChildren(element("p", "Etapa 00: implementa el CRUD de proyectos con el prompt 03. La autenticación ya está funcionando.", "help"));
  await loadExperiments();
}

function renderProjects() {
  $("#project-list").replaceChildren();
  if (!projects.length) $("#project-list").append(element("p", "Aún no tienes proyectos. Crea el primero.", "help"));
  projects.forEach((project) => {
    const button = element("button", project.name, `project-card${project.id === selectedId ? " active" : ""}`);
    button.setAttribute("aria-pressed", String(project.id === selectedId));
    button.append(element("small", project.description || "Sin descripción"));
    button.addEventListener("click", async () => {
      selectedId = project.id;
      $("#model-filter").value = "";
      renderProjects();
      try { await loadExperiments(); } catch (error) { notify(error.message); }
    });
    $("#project-list").append(button);
  });
}

async function loadExperiments() {
  const project = projects.find((item) => item.id === selectedId);
  $("#project-actions").hidden = !project;
  $("#experiment-tools").hidden = !project;
  $("#selected-name").textContent = project?.name || "Tu siguiente proyecto";
  $("#selected-description").textContent = project?.description || (project ? "Sin descripción." : "Crea un proyecto para comenzar tu bitácora.");
  experiments = [];
  renderExperiments();
  if (!project) return;
  const requestId = project.id;
  const model = $("#model-filter").value.trim();
  let result;
  try {
    result = await api(`/projects/${requestId}/experiments${model ? `?model=${encodeURIComponent(model)}` : ""}`);
  } catch (error) {
    if (selectedId !== requestId) return;
    $("#experiment-empty h3").textContent = error.status === 501 ? "Siguiente etapa: experimentos" : "No se pudieron cargar los experimentos";
    $("#experiment-empty p").textContent = error.status === 501 ? "Los proyectos funcionan. Usa el prompt 04 para conectar los experimentos con la base de datos." : error.message;
    if (error.status !== 501) throw error;
    return;
  }
  if (selectedId !== requestId) return;
  experiments = result;
  renderExperiments();
}

function renderExperiments() {
  $("#experiment-list").replaceChildren();
  $("#experiment-empty h3").textContent = "Todo empieza con una pregunta";
  $("#experiment-empty p").textContent = "Aquí aparecerán los experimentos de tu proyecto. Si aplicaste un filtro, prueba a limpiarlo.";
  $("#experiments-table").hidden = !experiments.length;
  $("#experiment-empty").hidden = Boolean(experiments.length);
  experiments.forEach((experiment) => {
    const row = element("tr");
    const name = element("td");
    name.append(element("strong", experiment.name), element("small", experiment.dataset_version));
    if (experiment.notes) name.append(element("small", experiment.notes));
    const metric = element("td", `${experiment.metric_value} ${experiment.metric_name}`);
    const actions = element("td"), buttons = element("div", undefined, "actions");
    const edit = element("button", "Editar", "ghost"), remove = element("button", "Eliminar", "ghost danger");
    edit.setAttribute("aria-label", `Editar ${experiment.name}`);
    remove.setAttribute("aria-label", `Eliminar ${experiment.name}`);
    edit.addEventListener("click", () => openExperiment(experiment));
    remove.addEventListener("click", async () => {
      if (!confirm(`¿Eliminar el experimento “${experiment.name}”?`)) return;
      try { await api(`/experiments/${experiment.id}`, { method: "DELETE" }); await refresh(); notify("Experimento eliminado."); }
      catch (error) { notify(error.message); }
    });
    buttons.append(edit, remove); actions.append(buttons);
    row.append(name, element("td", experiment.model), metric, actions);
    $("#experiment-list").append(row);
  });
}

function fillForm(form, values = {}) {
  form.reset();
  form.querySelector(".form-error").textContent = "";
  Object.entries(values).forEach(([key, value]) => { if (form.elements.namedItem(key)) form.elements.namedItem(key).value = value; });
}

function openProject(project = null) {
  editingProject = project;
  fillForm($("#project-form"), project || {});
  $("#project-dialog-title").textContent = project ? "Editar proyecto" : "Nuevo proyecto";
  $("#project-dialog").showModal();
}

function openExperiment(experiment = null) {
  editingExperiment = experiment;
  fillForm($("#experiment-form"), experiment || {});
  $("#experiment-dialog-title").textContent = experiment ? "Editar experimento" : "Nuevo experimento";
  $("#experiment-dialog").showModal();
}

$("#login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = event.target.querySelector("button"); button.disabled = true;
  $("#login-error").textContent = "";
  try {
    const user = await api("/auth/login", { method: "POST", body: JSON.stringify(Object.fromEntries(new FormData(event.target))) });
    event.target.reset();
    await enterWorkspace(user);
  } catch (error) { $("#login-error").textContent = error.message; notify(error.message); }
  finally { button.disabled = false; }
});

$("#logout").addEventListener("click", async () => {
  try { await api("/auth/logout", { method: "POST" }); showLogin(); }
  catch (error) { notify(error.message); }
});
$("#new-project").addEventListener("click", () => openProject());
$("#edit-project").addEventListener("click", () => openProject(projects.find((project) => project.id === selectedId)));
$("#new-experiment").addEventListener("click", () => openExperiment());
$("#filter-form").addEventListener("submit", async (event) => {
  event.preventDefault(); try { await loadExperiments(); } catch (error) { notify(error.message); }
});
$("#delete-project").addEventListener("click", async () => {
  if (!confirm("¿Eliminar este proyecto? Primero debe estar vacío.")) return;
  try { await api(`/projects/${selectedId}`, { method: "DELETE" }); selectedId = null; await refresh(); notify("Proyecto eliminado."); }
  catch (error) { notify(error.message); }
});
document.querySelectorAll(".close-dialog").forEach((button) => button.addEventListener("click", () => button.closest("dialog").close()));

for (const kind of ["project", "experiment"]) {
  $(`#${kind}-form`).addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.target, button = form.querySelector('[type="submit"]');
    button.disabled = true; form.querySelector(".form-error").textContent = "";
    const payload = Object.fromEntries(new FormData(form));
    const editing = kind === "project" ? editingProject : editingExperiment;
    if (kind === "experiment") payload.metric_value = Number(payload.metric_value);
    let path = kind === "project" ? "/projects" : `/projects/${selectedId}/experiments`;
    if (editing) path = `/${kind}s/${editing.id}`;
    try {
      const saved = await api(path, { method: editing ? "PUT" : "POST", body: JSON.stringify(payload) });
      if (kind === "project") selectedId = saved.id;
      form.closest("dialog").close();
      await refresh(); notify("Cambios guardados.");
    } catch (error) { form.querySelector(".form-error").textContent = error.message; }
    finally { button.disabled = false; }
  });
}

(async () => {
  try { await enterWorkspace(await api("/auth/me")); }
  catch (error) { if (!csrf) showLogin(); else notify(error.message); }
})();
