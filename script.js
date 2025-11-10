function calcular() {
    const tipo = document.getElementById('tipoImovel').value;
    const quartos = parseInt(document.getElementById('quartos').value);
    const garagem = document.getElementById('garagem').value;
    const vagas = parseInt(document.getElementById('vagas').value);
    const semFilhos = document.getElementById('semFilhos').value;
    const parcelas = parseInt(document.getElementById('parcelas').value);

    let aluguelBase = 0;

    if (tipo === 'casa') aluguelBase = 1200;
    else if (tipo === 'apartamento') aluguelBase = 1000;
    else if (tipo === 'kitnet') aluguelBase = 800;

    let valorQuartos = quartos * 150;
    let valorGaragem = garagem === 'sim' ? vagas * 100 : 0;
    let aluguelFinal = aluguelBase + valorQuartos + valorGaragem;

    // Aplicar desconto de 5% se não tiver filhos
    if (semFilhos === 'sim') {
        aluguelFinal *= 0.95;
    }

    const valorContrato = 2000;
    const parcelaContrato = valorContrato / parcelas;
    const totalMensal = aluguelFinal + parcelaContrato;
    const totalContrato = totalMensal * 12;

    document.getElementById('resultado').innerHTML = `
        <h3>Resultado:</h3>
        <p><strong>Tipo:</strong> ${tipo}</p>
        <p><strong>Quartos:</strong> ${quartos}</p>
        <p><strong>Garagem:</strong> ${garagem === 'sim' ? vagas + ' vaga(s)' : 'Não possui'}</p>
        <p><strong>Sem filhos:</strong> ${semFilhos === 'sim' ? 'Sim (5% de desconto aplicado)' : 'Não'}</p>
        <p><strong>Aluguel mensal:</strong> R$ ${aluguelFinal.toFixed(2)}</p>
        <p><strong>Parcela do contrato (${parcelas}x):</strong> R$ ${parcelaContrato.toFixed(2)}</p>
        <p><strong>Total mensal:</strong> R$ ${totalMensal.toFixed(2)}</p>
        <p><strong>Total anual (12 meses):</strong> R$ ${totalContrato.toFixed(2)}</p>
    `;
}

function limpar() {
    document.getElementById('formulario').reset();
    document.getElementById('resultado').innerHTML = '';
}

function gerarCSV() {
    const resultado = document.getElementById('resultado').innerText;
    if (!resultado) {
        alert('Calcule primeiro antes de gerar o CSV!');
        return;
    }
    const blob = new Blob([resultado], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'orcamento_aluguel.csv';
    link.click();
}
