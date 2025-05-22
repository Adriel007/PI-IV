// Grafico descritivo (pizza, barras, linhas)
const chartColors = [
  "rgb(255, 99, 132)", // rosa avermelhado
  "rgb(54, 162, 235)", // azul claro
  "rgb(255, 205, 86)", // amarelo
  "rgb(75, 192, 192)", // verde água
  "rgb(153, 102, 255)", // roxo claro
  "rgb(255, 159, 64)", // laranja
  "rgb(201, 203, 207)", // cinza claro
  "rgb(255, 99, 71)", // tomate
  "rgb(144, 238, 144)", // verde claro
  "rgb(255, 182, 193)", // rosa claro
  "rgb(70, 130, 180)", // azul aço
  "rgb(32, 178, 170)", // verde-mar escuro
  "rgb(218, 165, 32)", // dourado
  "rgb(0, 128, 128)", // teal
  "rgb(199, 21, 133)", // rosa escuro
  "rgb(173, 216, 230)", // azul claro
  "rgb(255, 140, 0)", // laranja escuro
  "rgb(152, 251, 152)", // verde pálido
  "rgb(0, 191, 255)", // azul profundo
  "rgb(219, 112, 147)", // rosa médio
  "rgb(205, 92, 92)", // vermelho indiano
  "rgb(186, 85, 211)", // roxo médio
  "rgb(240, 230, 140)", // cáqui
  "rgb(60, 179, 113)", // verde médio
  "rgb(244, 164, 96)", // salmão escuro
  "rgb(255, 228, 181)", // mocassim
  "rgb(0, 250, 154)", // verde-mar médio
  "rgb(147, 112, 219)", // roxo médio claro
  "rgb(176, 196, 222)", // azul claro acinzentado
  "rgb(255, 215, 0)", // ouro
  "rgb(233, 150, 122)", // salmão claro
  "rgb(100, 149, 237)", // azul acinzentado
  "rgb(127, 255, 212)", // azul turquesa claro
];

const plotChartSingle = (rawData) => {
  const cursos = [...new Set(rawData.map((row) => row.curso))];
  const periodos = [
    ...new Set(rawData.map((row) => `${row.ano}.${row.semestre}`)),
  ].sort();

  const datasets = cursos.map((curso, idx) => {
    const cor = chartColors[idx % chartColors.length];

    // Preenche os dados para cada período
    const data = periodos.map((periodo) => {
      const [ano, semestre] = periodo.split(".");
      const match = rawData.find(
        (r) => r.curso === curso && r.ano === ano && r.semestre === semestre
      );

      if (!match) return 0;

      return ["1° C", "2° C", "3° C", "4° C", "5° C", "6° C"].reduce(
        (sum, col) => sum + (parseFloat(match[col]) || 0),
        0
      );
    });

    return {
      label: curso,
      data,
      backgroundColor: cor,
      borderColor: cor,
      fill: false,
      tension: 0.3,
    };
  });

  // Gráfico de Linha
  const ctx_line = document
    .getElementById("chart-line-single")
    .getContext("2d");
  new Chart(ctx_line, {
    type: "line",
    data: {
      labels: periodos,
      datasets,
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Desistentes por semestre (por curso)",
        },
        legend: {
          position: "right",
        },
      },
    },
  });

  // Gráfico de Barras (stacked ou não)
  const ctx_bar = document.getElementById("chart-bar-single").getContext("2d");
  new Chart(ctx_bar, {
    type: "bar",
    data: {
      labels: periodos,
      datasets,
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Desistentes por semestre (por curso)",
        },
        legend: {
          position: "right",
        },
      },
    },
  });

  // Gráfico de Pizza (total de desistências por curso)
  const desistenciasTotais = datasets.map((ds) =>
    ds.data.reduce((sum, val) => sum + val, 0)
  );
  const ctx_pie = document.getElementById("chart-pie-single").getContext("2d");
  new Chart(ctx_pie, {
    type: "pie",
    data: {
      labels: cursos,
      datasets: [
        {
          data: desistenciasTotais,
          backgroundColor: cursos.map(
            (_, i) => chartColors[i % chartColors.length]
          ),
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Total de desistentes por curso",
        },
        legend: {
          position: "right",
        },
        datalabels: {
          formatter: (value, context) => {
            const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
            const percentage = (value / total * 100).toFixed(1) + '%';
            return `${percentage}\n(${value})`;
          },
          color: "#fff",
          font: {
            weight: "bold",
            size: 14
          },
          align: "center",
          anchor: "center",
        }
      }
    },
    plugins: [ChartDataLabels]
  });
  

const plotChart = (data) => {
  const ctx_pie = document.getElementById("chart-pie").getContext("2d");
  new Chart(ctx_pie, {
    type: "pie",
    data: {
      labels: data.labels,
      datasets: [
        {
          data: data.desistencias,
          backgroundColor: [...chartColors],
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
        datalabels: {
          formatter: (value, context) => {
            const total = context.chart.data.datasets[0].data.reduce(
              (a, b) => a + b,
              0
            );
            const percentage = ((value / total) * 100).toFixed(1) + "%";
            return `${percentage}\n(${value})`;
          },

          color: "#fff",
          font: {
            weight: "bold",
            size: 14,
          },
        },
      },
    },
    plugins: [ChartDataLabels],
  });

  const ctx_bar = document.getElementById("chart-bar").getContext("2d");
  new Chart(ctx_bar, {
    type: "bar",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: "Desistentes",
          data: data.desistencias,
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
          data: data.desistencias,
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

// EXAMPLE ////////////////////////////////////////

const cloudWord = (data) => {
  const ctx = document.getElementById("chart-wordCloud").getContext("2d");

  new Chart(ctx, {
    type: "wordCloud",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: "Frequência",
          data: data.values,
          color: chartColors,
        },
      ],
    },
    options: {
      responsive: false, // DESATIVAR responsividade
      maintainAspectRatio: false, // NÃO manter proporção
      plugins: {
        legend: {
          display: false,
        },
      },
    },
  });
};
