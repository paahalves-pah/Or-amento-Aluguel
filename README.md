# Simulador de Orçamento de Aluguel - R.M. Imobiliária

Projeto entregue para a disciplina "Algorithmic Thinking & Introduction to Object-Oriented Programming".

## Conteúdo
- `estimator.py` — versão Python OOP (CLI) que gera o orçamento e exporta `orcamento_12_parcelas.csv`.
- `web/index.html`, `web/styles.css`, `web/app.js` — versão frontend (puro JS) que calcula orçamentos e permite baixar CSV.
- `README.md` — este arquivo.
- `requirements.txt` — (vazio, sem dependências externas).

## Como usar

### Python (linha de comando)
```bash
python estimator.py
```
Siga as instruções interativas. Um arquivo `orcamento_12_parcelas.csv` será gerado na mesma pasta.

### Versão Web (local)
Abra `web/index.html` no seu navegador. A interface permite calcular e baixar o CSV com 12 parcelas.

## Observações de implementação
- O valor do contrato é R$ 2.000,00 e pode ser parcelado em até 5x.
- No CSV, as parcelas do contrato são distribuídas nos primeiros N meses (N = parcelas escolhidas).
- Desconto de 5% aplicado apenas para Apartamentos sem crianças.

## Autor
Projeto gerado por assistente automático a pedido do(a) estudante.
