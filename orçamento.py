import csv
import os
from datetime import datetime

class Imovel:
    def __init__(self, tipo, base_value, quartos=1):
        self.tipo = tipo
        self.base_value = base_value
        self.quartos = quartos
        self.garagem = False
        self.vagas_estudio = 0
        self.sem_criancas = False

    def calcular_mensal(self):
        valor = self.base_value
        # Extras for 2 quartos
        if self.tipo == "Apartamento" and self.quartos == 2:
            valor += 200
        if self.tipo == "Casa" and self.quartos == 2:
            valor += 250
        # Garagem for casas/apartamentos
        if self.garagem and self.tipo in ["Apartamento", "Casa"]:
            valor += 300
        # Estudio parking rules
        if self.tipo == "Estudio":
            if self.vagas_estudio >= 2:
                valor += 250
                extra = max(0, self.vagas_estudio - 2)
                valor += extra * 60
            elif self.vagas_estudio == 1:
                valor += 60
        # Discount for apartments without children
        if self.tipo == "Apartamento" and self.sem_criancas:
            valor *= 0.95
        return round(valor, 2)

def solicitar_opcoes():
    print("=== Simulador de Orçamento de Aluguel - R.M. Imobiliária ===")
    print("Tipos disponíveis:")
    print("1 - Apartamento (R$ 700,00 / 1 quarto)")
    print("2 - Casa (R$ 900,00 / 1 quarto)")
    print("3 - Estúdio (R$ 1200,00)")
    tipo_map = {"1": "Apartamento", "2": "Casa", "3": "Estudio"}

    escolha = input("Escolha o tipo (1/2/3): ").strip()
    while escolha not in tipo_map:
        escolha = input("Opção inválida. Escolha 1, 2 ou 3: ").strip()

    tipo = tipo_map[escolha]
    if tipo == "Apartamento":
        base = 700.0
    elif tipo == "Casa":
        base = 900.0
    else:
        base = 1200.0

    # Quartos
    quartos = 1
    if tipo in ["Apartamento", "Casa"]:
        q = input("Deseja 1 ou 2 quartos? (1/2) [1]: ").strip()
        if q == "2":
            quartos = 2

    imovel = Imovel(tipo, base, quartos)

    # Garagem
    if tipo in ["Apartamento", "Casa"]:
        g = input("Deseja vaga de garagem? (s/n) [n]: ").strip().lower()
        if g == "s":
            imovel.garagem = True
    else:  # Estudio
        v = input("Quantidade de vagas para o Estúdio (0,1,2,... ) [0]: ").strip()
        try:
            v_int = int(v) if v != "" else 0
        except:
            v_int = 0
        imovel.vagas_estudio = max(0, v_int)

    # Sem crianças (apenas relevante para apartamentos)
    if tipo == "Apartamento":
        sc = input("Sem crianças? (s/n) [n]: ").strip().lower()
        if sc == "s":
            imovel.sem_criancas = True

    # Contract installments
    contrato_total = 2000.0
    print("O valor do contrato é R$ 2.000,00 e pode ser parcelado em até 5x.")
    n_inst = input("Deseja parcelar o contrato em quantas vezes? (1-5) [1]: ").strip()
    try:
        n_inst_val = int(n_inst) if n_inst != "" else 1
    except:
        n_inst_val = 1
    if n_inst_val < 1:
        n_inst_val = 1
    if n_inst_val > 5:
        n_inst_val = 5

    return imovel, contrato_total, n_inst_val

def gerar_csv(imovel, contrato_total, n_inst, filename):
    mensal = imovel.calcular_mensal()
    contrato_parcela = round(contrato_total / n_inst, 2)
    rows = []
    hoje = datetime.today()
    for m in range(12):
        mes_data = datetime(hoje.year if hoje.month + m <= 12 else hoje.year + 1,
                            ((hoje.month + m - 1) % 12) + 1, 1)
        parcela_contrato = contrato_parcela if m < n_inst else 0.0
        total_mes = round(mensal + parcela_contrato, 2)
        rows.append({
            "mes": mes_data.strftime("%Y-%m"),
            "aluguel_mensal": f"{mensal:.2f}",
            "parcela_contrato": f"{parcela_contrato:.2f}",
            "total_a_pagar": f"{total_mes:.2f}"
        })

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["mes", "aluguel_mensal", "parcela_contrato", "total_a_pagar"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    return filename, rows

def main():
    imovel, contrato_total, n_inst = solicitar_opcoes()
    mensal = imovel.calcular_mensal()
    print("\n--- Orçamento Gerado ---")
    print(f"Tipo: {imovel.tipo}")
    print(f"Quartos: {imovel.quartos}")
    if imovel.tipo in ['Apartamento', 'Casa']:
        print(f"Garagem: {'Sim' if imovel.garagem else 'Não'}")
    if imovel.tipo == 'Estudio':
        print(f"Vagas Estúdio: {imovel.vagas_estudio}")
    print(f"Sem crianças (desconto aplica-se a apartamentos): {'Sim' if imovel.sem_criancas else 'Não'}")
    print(f"Aluguel mensal (estimado): R$ {mensal:.2f}")
    print(f"Valor do contrato: R$ {contrato_total:.2f} (parcelado em {n_inst}x -> R$ {contrato_total / n_inst:.2f} por parcela)")

    salvar = input("Deseja gerar CSV com as 12 parcelas do orçamento? (s/n) [s]: ").strip().lower()
    if salvar != "n":
        filename = os.path.join(os.path.dirname(__file__), "orcamento_12_parcelas.csv")
        filepath, rows = gerar_csv(imovel, contrato_total, n_inst, filename)
        print(f"CSV gerado: {filepath}")
    print("\nObrigado por usar o Simulador R.M. Imobiliária!")

if __name__ == '__main__':
    main()
