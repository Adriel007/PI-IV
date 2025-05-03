// Grafico descritivo (pizza, barras, linhas)
const plotChart = (data) => {
  console.log(data);
  const ctx_pie = document.getElementById("chart-pie").getContext("2d");
  new Chart(ctx_pie, {
    type: "pie",
    data: {
      labels: data.labels,
      datasets: [
        {
          data: data.values,
          backgroundColor: [
            "rgb(255, 99, 132)",
            "rgb(54, 162, 235)",
            "rgb(255, 205, 86)",
            "rgb(75, 192, 192)",
            "rgb(153, 102, 255)",
            "rgb(255, 159, 64)",
          ],
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "right",
        },
        title: {
          display: true,
          text: "Distribuição dos alunos por semestre",
        },
      },
    },
  });

  const ctx_bar = document.getElementById("chart-bar").getContext("2d");
  new Chart(ctx_bar, {
    type: "bar",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: "Desistentes",
          data: data.values,
          backgroundColor: "rgb(255, 99, 132)",
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "right",
        },
        title: {
          display: true,
          text: "Desistentes por semestre",
        },
      },
    },
  });

  const ctx_line = document.getElementById("chart-line").getContext("2d");
  new Chart(ctx_line, {
    type: "line",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: "Desistentes",
          data: data.values,
          borderColor: "rgb(255, 99, 132)",
          tension: 0.3,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "right",
        },
        title: {
          display: true,
          text: "Desistentes por semestre",
        },
      },
    },
  });
};

// Gráfico - histórico + previsão IA (vindos do Python)
const plotChartIA = (data) => {
  // Gráfico histórico + previsão
  const ctx1 = document.getElementById("chart-historical").getContext("2d");

  new Chart(ctx1, {
    type: "line",
    data: {
      labels: [...data.historical_data.labels, ...data.future_labels],
      datasets: [
        {
          label: "Histórico",
          data: data.historical_data.values,
          borderColor: "blue",
          tension: 0.3,
        },
        {
          label: "Previsão",
          data: [
            ...Array(data.historical_data.labels.length).fill(null),
            ...data.future_predictions,
          ],
          borderColor: "red",
          borderDash: [5, 5],
          tension: 0.3,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Desistências: Histórico e Previsão",
        },
      },
    },
  });

  // Heatmap de correlação
  const ctx2 = document.getElementById("chart-correlation").getContext("2d");
  const labels = data.correlation_data.labels;
  const matrix = data.correlation_data.data;

  const heatmapData = [];
  for (let y = 0; y < labels.length; y++) {
    for (let x = 0; x < labels.length; x++) {
      heatmapData.push({
        x: labels[x],
        y: labels[y],
        v: matrix[y][x],
      });
    }
  }

  new Chart(ctx2, {
    type: "matrix",
    data: {
      datasets: [
        {
          label: "Correlação",
          data: heatmapData,
          backgroundColor(ctx) {
            const value = ctx.dataset.data[ctx.dataIndex].v;
            const alpha = Math.abs(value);
            if (value > 0)
              return `rgba(0, 0, 255, ${alpha})`; // Azul para correlação positiva
            else return `rgba(255, 0, 0, ${alpha})`; // Vermelho para negativa
          },
          borderColor: "black",
          borderWidth: 0.5,
          width: ({ chart }) =>
            (chart.chartArea || {}).width / labels.length - 1,
          height: ({ chart }) =>
            (chart.chartArea || {}).height / labels.length - 1,
        },
      ],
      labels: labels,
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: "Matriz de Correlação (Heatmap)",
        },
        tooltip: {
          callbacks: {
            title: (items) => {
              const item = items[0];
              return `${item.raw.y} vs ${item.raw.x}`;
            },
            label: (item) => `Correlação: ${item.raw.v.toFixed(2)}`,
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

const clearChart = () => {
  const oldCanvas = document.getElementById("dropoutChart");
  if (oldCanvas) oldCanvas.remove();
};

const showModelInfo = (modelInfo) => {
  if (!modelInfo || !modelInfo.bestModel || !modelInfo.metrics) {
    Swal.fire({
      title: "Informações do Modelo",
      text: "Nenhuma informação de modelo disponível.",
      icon: "info",
      confirmButtonText: "OK",
    });
    return;
  }

  let infoText = `<strong>Modelo utilizado:</strong> ${modelInfo.bestModel}`;

  infoText += `<br><br><strong>Métricas:</strong>`;
  for (const [modelName, metrics] of Object.entries(modelInfo.metrics)) {
    infoText += `<br>• ${modelName}: RMSE = ${
      metrics.cv_rmse?.toFixed(2) || "N/A"
    }`;
  }

  Swal.fire({
    title: "Informações do Modelo",
    html: infoText,
    icon: "info",
    confirmButtonText: "OK",
  });
};
