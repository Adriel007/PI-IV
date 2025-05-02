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

  if (result.correlation_data) {
    plotCorrelationMatrix(result.correlation_data);
  }

  plotChart({
    labels: [...result.historical_data.labels, ...result.future_labels],
    desistencias: [
      ...result.historical_data.values,
      ...result.future_predictions,
    ],
    predictedStartIndex: result.historical_data.labels.length,
  });
};

const clearChart = () => {
  const oldCanvas = document.getElementById("dropoutChart");
  if (oldCanvas) oldCanvas.remove();
};

const showModelInfo = (modelInfo) => {
  if (modelInfo) {
    if (!modelInfo) return;

    // Cria um texto formatado com as informações do modelo
    let infoText = `<strong>Modelo utilizado:</strong> ${
      modelInfo.bestModel || "N/A"
    }`;

    if (modelInfo.metrics) {
      infoText += `<br><br><strong>Métricas:</strong>`;
      for (const [modelName, metrics] of Object.entries(modelInfo.metrics)) {
        infoText += `<br>• ${modelName}: RMSE = ${
          metrics.cv_rmse?.toFixed(2) || "N/A"
        }`;
      }
    }

    // Mostra as informações usando SweetAlert2
    Swal.fire({
      title: "Informações do Modelo",
      html: infoText,
      icon: "info",
      confirmButtonText: "OK",
    });
  } else {
    // Se nenhuma informação do modelo for disponível, mostra uma mensagem de aviso
    Swal.fire({
      title: "Informações do Modelo",
      text: "Nenhuma informação do modelo disponível.",
      icon: "info",
      confirmButtonText: "OK",
    });
  }
};

const plotCorrelationMatrix = ({ labels, data }) => {
  const ctxId = "correlationChart";
  const oldCanvas = document.getElementById(ctxId);
  if (oldCanvas) oldCanvas.remove();

  const canvas = document.createElement("canvas");
  canvas.id = ctxId;
  document.getElementById("analise-content").appendChild(canvas);
  const ctx = canvas.getContext("2d");

  new Chart(ctx, {
    type: "matrix", // Requer o plugin chartjs-chart-matrix
    data: {
      datasets: [
        {
          label: "Correlação",
          data: data
            .map((row, i) =>
              row.map((value, j) => ({
                x: j,
                y: i,
                v: value,
              }))
            )
            .flat(),
          backgroundColor: (ctx) => {
            const value = ctx.raw.v;
            const alpha = Math.abs(value); // Use alpha to show intensity
            return `rgba(0, 0, 255, ${alpha})`;
          },
          width: ({ chart }) =>
            (chart.chartArea || {}).width / labels.length - 1,
          height: ({ chart }) =>
            (chart.chartArea || {}).height / labels.length - 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Matriz de Correlação",
          font: { size: 20 },
        },
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => `Valor: ${ctx.raw.v.toFixed(2)}`,
          },
        },
      },
      scales: {
        x: {
          type: "category",
          labels: labels,
          offset: true,
          grid: { display: false },
        },
        y: {
          type: "category",
          labels: labels,
          offset: true,
          grid: { display: false },
        },
      },
    },
  });
};
