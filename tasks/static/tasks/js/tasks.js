async function loadTasks() {
  const res = await fetch("/api/tasks/");
  const tasks = await res.json();

  const tbody = document.getElementById("task-body");
  tbody.innerHTML = "";

  tasks.forEach((task, index) => {
    tbody.innerHTML += `
      <tr>
        <td>${index + 1}</td>
        <td>${task.title}</td>
        <td>${task.description}</td>
        <td>${task.due_date || ""}</td>
        <td>
          <select class="${task.status === 'done' ? 'done' : 'pending'}" onchange="updateStatus(${task.id}, this.value)">
            <option value="pending" ${task.status === "pending" ? "selected" : ""}>Pending</option>
            <option value="done" ${task.status === "done" ? "selected" : ""}>Done</option>
          </select>
        </td>
        <td>
          <button id="delete-button" onclick="deleteTask(${task.id})">Delete</button>
        </td>
      </tr>
    `;
  });
}

async function createTask() {
  const title = document.querySelector("[name=title]").value;
  const description = document.querySelector("[name=description]").value;
  const due_date = document.querySelector("[name=due_date]").value;

  await fetch("/api/tasks/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, description, due_date })
  });

  loadTasks();
}

async function updateStatus(id, status) {
  await fetch(`/api/tasks/${id}/`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status })
  });

  loadTasks();
}

async function deleteTask(id) {
  await fetch(`/api/tasks/${id}/`, { method: "DELETE" });
  loadTasks();
}

document.addEventListener("DOMContentLoaded", loadTasks);

document
  .getElementById("create-task-form")
  .addEventListener("submit", function (e) {
    e.preventDefault();  // stop page reload
    createTask();
    this.reset();        // 🔥 clears form
  });
