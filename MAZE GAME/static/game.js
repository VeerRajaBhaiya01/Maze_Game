let gridDiv = document.getElementById("grid");

document.addEventListener("keydown", e => {
  const dir = {ArrowUp: "up", ArrowDown: "down", ArrowLeft: "left", ArrowRight: "right"}[e.key];
  if (dir) {
    fetch("/move", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({direction: dir})
    })
    .then(res => res.json())
    .then(updateGrid);
  }
});

function updateGrid(data) {
  document.getElementById("score").innerText = data.score;
  document.getElementById("level").innerText = data.level;
  document.getElementById("target").innerText = data.target_score;
  document.getElementById("status").innerText = data.status;

  gridDiv.innerHTML = "";
  for (let i = 0; i < data.grid.length; i++) {
    for (let j = 0; j < data.grid[0].length; j++) {
      const cell = document.createElement("div");
      cell.className = `cell ${data.grid[i][j]}`;
      if (data.grid[i][j] === "reward") {
        const key = `${i},${j}`;
        cell.innerText = data.rewards[key];
      }
      gridDiv.appendChild(cell);
    }
  }
}
