let dadosCSV = [];
let chartCursos, chartBarras, chartLinha;

const colunasDesistencia = ["1° C", "2° C", "3° C", "4° C", "5° C", "6° C"];

const gerarCorHSL = (index, total) => `hsl(${(index * 360) / total}, 70%, 60%)`;

const somarDesistencias = (dado) =>
  colunasDesistencia.reduce(
    (soma, col) => soma + parseFloat(dado[col] || 0),
    0
  );

const loadFilters = (dados) => {
  const cursos = [...new Set(dados.map((d) => d.curso))];
  const anos = [...new Set(dados.map((d) => d.ano))].sort();

  const gerarOptions = (valores) =>
    `<option value="">Todos</option>` +
    valores.map((v) => `<option value="${v}">${v}</option>`).join("");

  document.getElementById("filtroCurso").innerHTML = gerarOptions(cursos);
  document.getElementById("filtroAno").innerHTML = gerarOptions(anos);
};

const applyFilters = () => {
  const curso = document.getElementById("filtroCurso").value;
  const ano = document.getElementById("filtroAno").value;
  return dadosCSV.filter(
    (d) => (!curso || d.curso === curso) && (!ano || d.ano.toString() === ano)
  );
};

const destroyCharts = () => {
  [chartCursos, chartBarras, chartLinha].forEach((c) => c?.destroy());
};

const atualizarGraficos = () => {
  const dadosFiltrados = applyFilters();
  destroyCharts();
  chartCursos = plotPieChartCursos(dadosFiltrados);
  chartBarras = plotBarChartAno(dadosFiltrados);
  chartLinha = plotLineChartCursos(dadosFiltrados);
};

// --- GRÁFICOS ---

const plotPieChartCursos = (dados) => {
  const ctx = document.getElementById("chart-cursos").getContext("2d");
  const contagem = {};

  dados.forEach((d) => {
    contagem[d.curso] = (contagem[d.curso] || 0) + 1;
  });

  const labels = Object.keys(contagem);
  const data = Object.values(contagem);

  return new Chart(ctx, {
    type: "pie",
    data: {
      labels,
      datasets: [
        {
          label: "Distribuição de Cursos",
          data,
          backgroundColor: labels.map((_, i) => gerarCorHSL(i, labels.length)),
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Distribuição por Curso",
        },
      },
    },
  });
};

const plotBarChartAno = (dados) => {
  const ctx = document.getElementById("chart-barras").getContext("2d");
  const porAno = {};

  dados.forEach((d) => {
    const ano = d.ano;
    porAno[ano] = (porAno[ano] || 0) + somarDesistencias(d);
  });

  const labels = Object.keys(porAno);
  const data = Object.values(porAno);

  return new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Desistências",
          data,
          backgroundColor: "rgba(255, 99, 132, 0.6)",
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Desistências por Ano",
        },
      },
    },
  });
};

const plotLineChartCursos = (dados) => {
  const ctx = document.getElementById("chart-tendencia").getContext("2d");
  const agrupado = {};
  const anos = [...new Set(dados.map((d) => d.ano))].sort();

  dados.forEach((d) => {
    const { curso, ano } = d;
    agrupado[curso] = agrupado[curso] || {};
    agrupado[curso][ano] = (agrupado[curso][ano] || 0) + somarDesistencias(d);
  });

  const cursos = Object.keys(agrupado);
  const datasets = cursos.map((curso, i) => ({
    label: curso,
    data: anos.map((ano) => agrupado[curso][ano] || 0),
    fill: false,
    borderColor: gerarCorHSL(i, cursos.length),
    tension: 0.3,
  }));

  return new Chart(ctx, {
    type: "line",
    data: {
      labels: anos,
      datasets,
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Tendência de Desistências por Curso",
        },
      },
    },
  });
};

const inicializarGraficos = (dados) => {
  dadosCSV = dados;
  loadFilters(dados);
  atualizarGraficos();
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
