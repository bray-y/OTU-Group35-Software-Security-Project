const container = document.getElementById("role-container");
const API_BASE = "http://127.0.0.1:5000"; // Python backend

function openPage(role) {
  container.innerHTML = ""; // Clear previous content

  if (role === "purchaser") {
    container.innerHTML = `
      <div class="role-card">
        <h2>Purchaser</h2>
        <label>Item</label><input id="item">
        <label>Quantity</label><input id="qty">
        <label>Price</label><input id="price">
        <label>Department</label><input id="dept">
        <label>Justification</label><input id="just">
        <button onclick="sendOrder()">Send Secure Order</button>
        <p id="message" class="success-message"></p>
      </div>
    `;
  } else if (role === "supervisor") {
    container.innerHTML = `
      <div class="role-card">
        <h2>Supervisor</h2>
        <button onclick="loadOrder()">Load Order</button>
        <div style="max-height:300px; overflow:auto; border:1px solid #ccc; padding:10px; margin:10px 0;">
          <pre id="order-data"></pre>
        </div>
        <button onclick="approveOrder()">Approve</button>
        <p id="message" class="success-message"></p>
      </div>
    `;
  } else if (role === "dept") {
    container.innerHTML = `
      <div class="role-card">
        <h2>Purchasing Dept</h2>
        <button onclick="verifyOrder()">Verify Final Order</button>
        <div style="max-height:200px; overflow:auto; border:1px solid #ccc; padding:10px; margin-top:10px;">
          <p id="message" class="success-message"></p>
        </div>
      </div>
    `;
  } else if (role === "audit") {
    container.innerHTML = `
      <div class="role-card">
        <h2>Audit Log</h2>
        <button onclick="loadLogs()">Refresh Log</button>
        <div style="max-height:300px; overflow:auto; border:1px solid #ccc; padding:10px; margin-top:10px;">
          <ul id="logs"></ul>
        </div>
      </div>
    `;
  }
}

// ---------------------- Purchaser ----------------------
function sendOrder() {
  const data = {
    item: document.getElementById("item").value,
    quantity: document.getElementById("qty").value,
    price: document.getElementById("price").value,
    department: document.getElementById("dept").value,
    justification: document.getElementById("just").value,
  };

  fetch(`${API_BASE}/purchaser/order`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then(res => res.json())
    .then(() => {
      document.getElementById("message").innerText = "Order sent securely!";
    })
    .catch(err => console.error(err));
}

// ---------------------- Supervisor ----------------------
function loadOrder() {
  fetch(`${API_BASE}/supervisor/load_order`)
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        document.getElementById("order-data").innerText = data.error;
      } else {
        // Optional: truncate signature for display
        const displayData = { ...data };
        if (displayData.signature) {
          displayData.signature =
            displayData.signature.slice(0, 30) +
            "... (" +
            displayData.signature.length +
            " chars)";
        }
        document.getElementById("order-data").innerText = JSON.stringify(displayData, null, 2);
      }
    })
    .catch(err => console.error(err));
}

function approveOrder() {
  fetch(`${API_BASE}/supervisor/approve`, { method: "POST" })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        document.getElementById("message").innerText = data.error;
      } else {
        document.getElementById("message").innerText = "Order approved securely!";
      }
    })
    .catch(err => console.error(err));
}

// ---------------------- Dept ----------------------
function verifyOrder() {
  fetch(`${API_BASE}/dept/verify`, { method: "POST" })
    .then(res => res.json())
    .then(data => {
      const msgEl = document.getElementById("message");
      if (data.error) {
        msgEl.innerText = data.error;
      } else {
        msgEl.innerText = "Order fully verified!";
      }
    })
    .catch(err => console.error(err));
}

// ---------------------- Audit ----------------------
function loadLogs() {
  fetch(`${API_BASE}/audit/logs`)
    .then(res => res.json())
    .then(logs => {
      const logsEl = document.getElementById("logs");
      logsEl.innerHTML = logs.map(log => `<li>${log}</li>`).join("");
    })
    .catch(err => console.error(err));
}