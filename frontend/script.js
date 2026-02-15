const API = "http://127.0.0.1:8000";

// ================= LOAD DRUG LIST (dropdown awal) =================
async function loadDrugs() {
    let res = await fetch(`${API}/all_drugs`);
    let data = await res.json();

    let list = document.getElementById("drugOptions");
    list.innerHTML = "";

    data.forEach(drug => {
        let opt = document.createElement("option");
        opt.value = drug;
        list.appendChild(opt);
    });
}

loadDrugs();

// ================= SAAT OBAT DIPILIH → LOAD INTERACT =================
document.getElementById("drugInput").addEventListener("change", loadInteractions);
document.getElementById("drugInput").addEventListener("input", loadInteractions);

async function loadInteractions() {
    let drug = document.getElementById("drugInput").value;
    if (!drug) return;

    let res = await fetch(`${API}/interactions_by_drug?drug=${encodeURIComponent(drug)}`);
    let data = await res.json();

    let list = document.getElementById("interactOptions");
    list.innerHTML = "";

    data.forEach(item => {
        let opt = document.createElement("option");
        opt.value = item;
        list.appendChild(opt);
    });
}

// ================= CHECK INTERACTION =================
async function checkInteraction() {
    let drug = document.getElementById("drugInput").value.trim();
    let interact = document.getElementById("interactInput").value.trim();

    if (!drug || !interact) {
        alert("Lengkapi dulu obat dan interaksi");
        return;
    }

    let res = await fetch(
        `${API}/check?name=${encodeURIComponent(drug)}&interact=${encodeURIComponent(interact)}`
    );

    let data = await res.json();
    let box = document.getElementById("result");
    box.style.display = "block";

    if (data.message) {
        box.innerHTML = "❌ Interaksi tidak ditemukan di database";
        return;
    }

    let sevColor = "#22c55e";
    if (data.severity.toLowerCase().includes("major")) sevColor = "#ef4444";
    else if (data.severity.toLowerCase().includes("moderate")) sevColor = "#f59e0b";

    box.innerHTML = `
    <h2>💊 Hasil Interaksi</h2>
    <p><b>Severity:</b> <span style="color:${sevColor};font-weight:bold">${data.severity}</span></p>
    <p><b>Description:</b><br>${data.interaction_description}</p>
    <p><b>Recommendation:</b><br>${data.recommendation}</p>
  `;
}
