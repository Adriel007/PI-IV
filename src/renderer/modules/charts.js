// Gráfico - histórico e previsão simples
const plotChart = ({ labels, desistencias, predictedStartIndex }) => {
  const ctxId = "dropoutChart";
  const oldCanvas = document.getElementById(ctxId);
  if (oldCanvas) oldCanvas.remove();

  const canvas = document.createElement("canvas");
  canvas.id = ctxId;
  document.getElementById("analise-content").appendChild(canvas);

  const ctx = canvas.getContext("2d");

  const historicalData = desistencias.slice(0, predictedStartIndex);
  const predictedData = desistencias.slice(predictedStartIndex);

  new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Histórico de Desistências",
          data: [...historicalData, ...Array(predictedData.length).fill(null)],
          borderColor: "#2563eb",
          backgroundColor: "rgba(37,99,235,0.2)",
          tension: 0.3,
          fill: false,
          pointBackgroundColor: "#2563eb",
          pointRadius: 4,
        },
        {
          label: "Previsão Simples",
          data: [...Array(historicalData.length).fill(null), ...predictedData],
          borderColor: "#f97316",
          borderDash: [5, 5],
          backgroundColor: "rgba(249,115,22,0.2)",
          tension: 0.3,
          fill: false,
          pointBackgroundColor: "#f97316",
          pointRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Histórico vs Previsão Simples",
          font: {
            size: 20,
          },
        },
        legend: {
          display: true,
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Número de Desistentes",
          },
        },
        x: {
          title: {
            display: true,
            text: "Ano.Semestre",
          },
        },
      },
    },
  });
};

// Gráfico - histórico + previsão IA (vindos do Python)
const plotChartIA = ({ future_labels, future_predictions }) => {
  const ctxId = "dropoutChart";
  const oldCanvas = document.getElementById(ctxId);
  if (oldCanvas) oldCanvas.remove();

  const canvas = document.createElement("canvas");
  canvas.id = ctxId;
  document.getElementById("analise-content").appendChild(canvas);

  const ctx = canvas.getContext("2d");

  new Chart(ctx, {
    type: "line",
    data: {
      labels: future_labels,
      datasets: [
        {
          label: "Previsão IA",
          data: future_predictions,
          borderColor: "#10b981",
          backgroundColor: "rgba(16,185,129,0.2)",
          tension: 0.4,
          fill: true,
          pointBackgroundColor: "#059669",
          pointRadius: 5,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Previsão de Desistências via IA",
          font: {
            size: 20,
          },
        },
        legend: {
          display: true,
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Número de Desistentes",
          },
        },
        x: {
          title: {
            display: true,
            text: "Ano.Semestre",
          },
        },
      },
    },
  });
};
