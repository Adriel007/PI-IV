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
      ...result,
      modelInfo: {
        bestModel: result.best_model,
        metrics: result.model_metrics,
      },
    };
  } catch (error) {
    console.error("Erro na análise Python:", error);
  }
};
