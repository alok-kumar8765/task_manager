const socket = io();

let cpu, mem, disk, gpu;

// Simple Gauge Builder
function createGauge(id, label) {
    return new Chart(document.getElementById(id), {
        type: "doughnut",
        data: {
            labels: [label, ""],
            datasets: [{
                data: [0, 100],
                backgroundColor: ["#00c8ff", "#333"]
            }]
        },
        options: { cutout: "70%" }
    });
}

cpu = createGauge("cpuGauge", "CPU");
mem = createGauge("memGauge", "Memory");
disk = createGauge("diskGauge", "Disk");
gpu = createGauge("gpuGauge", "GPU");


// Apply theme
function toggleTheme() {
    document.body.classList.toggle("dark");
    document.body.classList.toggle("light");

    fetch("/api/theme", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            theme: document.body.classList.contains("dark") ? "dark" : "light"
        })
    });
}


// Receive updates
socket.on("update", data => {

    // Update Gauges
    cpu.data.datasets[0].data[0] = data.cpu;
    mem.data.datasets[0].data[0] = data.mem;
    disk.data.datasets[0].data[0] = data.disk;
    gpu.data.datasets[0].data[0] = parseInt(data.gpu) || 0;

    cpu.update(); mem.update(); disk.update(); gpu.update();


    // Update Process Table
    let table = document.getElementById("processTable");
    table.innerHTML = "<tr><th>PID</th><th>Name</th><th>CPU %</th><th>Memory %</th></tr>";

    data.processes.forEach(p => {
        table.innerHTML += `
            <tr>
                <td>${p.pid}</td>
                <td>${p.name}</td>
                <td>${p.cpu}</td>
                <td>${p.mem.toFixed(1)}</td>
            </tr>
        `;
    });

    // Update Logs
    let logs = document.getElementById("logs");
    logs.innerHTML = data.logs.join("<br>");
});
