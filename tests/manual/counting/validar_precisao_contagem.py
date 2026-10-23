import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SENTIDOS = (
    "lado_negativo_para_positivo",
    "lado_positivo_para_negativo",
)


def carregar_json(caminho):
    with caminho.open("r", encoding="utf-8-sig") as arquivo:
        return json.load(arquivo)


def validar_dados(dados, nome):
    if not isinstance(dados, dict):
        raise ValueError(f"{nome}: esperado um objeto JSON.")

    for sentido in SENTIDOS:
        valor = dados.get(sentido)
        if isinstance(valor, bool) or not isinstance(valor, int) or valor < 0:
            raise ValueError(
                f"{nome}: '{sentido}' deve ser um inteiro >= 0."
            )


def calcular_metricas(manual, automatico):
    validar_dados(manual, "Contagem manual")
    validar_dados(automatico, "Contagem automática")

    resultado = {}
    total_manual = sum(manual[s] for s in SENTIDOS)
    total_automatico = sum(automatico[s] for s in SENTIDOS)

    for sentido in SENTIDOS:
        referencia = manual[sentido]
        detectado = automatico[sentido]
        diferenca = detectado - referencia

        resultado[sentido] = {
            "manual": referencia,
            "automatico": detectado,
            "diferenca_automatico_menos_manual": diferenca,
            "erro_absoluto": abs(diferenca),
            "erro_percentual": (
                round(abs(diferenca) / referencia * 100, 2)
                if referencia > 0
                else None
            ),
        }

    diferenca_total = total_automatico - total_manual

    return {
        "total_manual": total_manual,
        "total_automatico": total_automatico,
        "diferenca_automatico_menos_manual": diferenca_total,
        "erro_absoluto_total": abs(diferenca_total),
        "erro_percentual_total": (
            round(abs(diferenca_total) / total_manual * 100, 2)
            if total_manual > 0
            else None
        ),
        "por_sentido": resultado,
        "observacao": (
            "Comparação de totais não identifica, sozinha, "
            "veículos duplicados ou erros individuais de sentido."
        ),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Compara a contagem manual e automática do RoadVision."
    )
    parser.add_argument(
        "--manual",
        type=Path,
        default=ROOT / "data/resultados/counting/contagem_manual.json",
    )
    parser.add_argument(
        "--automatico",
        type=Path,
        default=ROOT / "data/resultados/counting/contagem_automatica.json",
    )
    parser.add_argument(
        "--saida",
        type=Path,
        default=ROOT / "data/resultados/counting/validacao_contagem.json",
    )
    args = parser.parse_args()

    if not args.manual.is_file():
        parser.error(f"Arquivo de contagem manual não encontrado: {args.manual}")
    if not args.automatico.is_file():
        parser.error(
            f"Arquivo de contagem automática não encontrado: {args.automatico}"
        )

    manual = carregar_json(args.manual)
    automatico = carregar_json(args.automatico)
    relatorio = calcular_metricas(manual, automatico)

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    with args.saida.open("w", encoding="utf-8") as arquivo:
        json.dump(relatorio, arquivo, ensure_ascii=False, indent=2)
        arquivo.write("\n")

    print(json.dumps(relatorio, ensure_ascii=False, indent=2))
    print(f"\nRelatório salvo em: {args.saida}")


if __name__ == "__main__":
    main()
