const parseCSV = (content) => {
  const lines = content.split("\n").filter((line) => line.trim() !== "");
  const headers = lines[0].split(",").map((h) => h.trim());
  return lines.slice(1).map((line) => {
    const values = line.split(",").map((v) => v.trim());
    const obj = {};
    headers.forEach((header, index) => {
      obj[header] = values[index];
    });
    return obj;
  });
};

const validateData = (data) => {
  const requiredColumns = [
    "curso",
    "semestre",
    "ano",
    "1° C",
    "2° C",
    "3° C",
    "4° C",
    "5° C",
    "6° C",
  ];
  if (!data.length) return false;
  const sample = data[0];
  return requiredColumns.every((col) => col in sample);
};

const processData = (data) => {
  const resumo = {};

  data.forEach((row) => {
    const ano = parseInt(row["ano"]);
    const semestre = parseInt(row["semestre"]);

    // Calcular o total de desistências somando todas as colunas de 1° C a 6° C
    const desistentes = ["1° C", "2° C", "3° C", "4° C", "5° C", "6° C"].reduce(
      (total, col) => total + (parseFloat(row[col]) || 0),
      0
    );

    if (!resumo[ano]) {
      resumo[ano] = { 1: 0, 2: 0 };
    }
    resumo[ano][semestre] += desistentes;
  });

  const labels = [];
  const desistencias = [];

  Object.keys(resumo)
    .sort((a, b) => parseInt(a) - parseInt(b))
    .forEach((ano) => {
      [1, 2].forEach((semestre) => {
        labels.push(`${ano}.${semestre}`);
        desistencias.push(resumo[ano][semestre]);
      });
    });

  return { labels, desistencias };
};

// dataProcessing.js
const predictFuture = async ({ labels, desistencias }) => {
  // Prepara os dados no formato esperado pelo Python (CSV)
  const csvContent = ["ano,semestre,desistentes"]; // Cabeçalho

  // Converte os dados históricos para o formato CSV
  labels.forEach((label, index) => {
    const [ano, semestre] = label.split(".");
    csvContent.push(`${ano},${semestre},${desistencias[index]}`);
  });

  const csvString = csvContent.join("\n");

  try {
    // Chama a análise via Python
    const result = await window.electronAPI.analisarDados(csvString);

    // Processa os resultados
    return {
      labels: [...labels, ...result.future_labels],
      desistencias: [...desistencias, ...result.future_predictions],
      predictedStartIndex: labels.length,
      modelInfo: {
        bestModel: result.best_model,
        metrics: result.model_metrics,
      },
    };
  } catch (error) {
    console.error("Erro na análise Python:", error);
    // Fallback para o método simples se o Python falhar
    return simplePredictFuture({ labels, desistencias });
  }
};

// Método simples de fallback
const simplePredictFuture = ({ labels, desistencias }) => {
  const futureLabels = [];
  const futureValues = [];

  if (desistencias.length < 2) {
    console.warn("Poucos dados para prever tendências.");
    return { labels, desistencias, predictedStartIndex: labels.length };
  }

  const n = desistencias.length;
  const last2 = desistencias.slice(-2);
  const growthRate = last2[1] - last2[0];

  let [lastYear, lastSemester] = labels[labels.length - 1]
    .split(".")
    .map(Number);

  for (let i = 0; i < 6; i++) {
    if (lastSemester === 1) {
      lastSemester = 2;
    } else {
      lastSemester = 1;
      lastYear += 1;
    }
    futureLabels.push(`${lastYear}.${lastSemester}`);
    const predicted =
      desistencias[desistencias.length - 1] + growthRate * (i + 1);
    futureValues.push(Math.max(0, Math.round(predicted)));
  }

  return {
    labels: [...labels, ...futureLabels],
    desistencias: [...desistencias, ...futureValues],
    predictedStartIndex: labels.length,
    modelInfo: {
      bestModel: "Simple Linear Projection",
      metrics: {},
    },
  };
};
