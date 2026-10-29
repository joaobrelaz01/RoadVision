
from datetime import datetime

from roadvision.database.supabase_client import supabase
from roadvision.database.validar_contagens import validar_contagem


def buscar_registros(tabela):
    """Busca os registros em páginas de até 1.000."""
    registros = []
    inicio = 0

    while True:
        resposta = (
            supabase.table(tabela)
            .select("*")
            .range(inicio, inicio + 999)
            .execute()
        )

        registros.extend(resposta.data)

        if len(resposta.data) < 1000:
            break

        inicio += 1000

    return registros


def executar_auditoria():
    cameras = buscar_registros("cameras")
    contagens = buscar_registros("contagens_minuto")

    ids_cameras = {str(camera["id"]) for camera in cameras}
    chaves = set()
    problemas = []

    for registro in contagens:
        erros = validar_contagem(registro)

        camera_id = str(registro.get("camera_id"))

        if camera_id not in ids_cameras:
            erros.append("Câmera não cadastrada")

        try:
            datetime.fromisoformat(
                registro["data_hora"].replace("Z", "+00:00")
            )
        except (ValueError, TypeError, KeyError):
            erros.append("Data e hora inválidas")

        chave = (camera_id, registro.get("data_hora"))

        if chave in chaves:
            erros.append("Registro duplicado")
        chaves.add(chave)

        if erros:
            problemas.append({
                "id": registro.get("id"),
                "erros": erros,
            })

    print(f"Câmeras cadastradas: {len(cameras)}")
    print(f"Contagens analisadas: {len(contagens)}")
    print(f"Registros com problemas: {len(problemas)}")

    for problema in problemas:
        print(problema)

    if not problemas:
        print("Auditoria concluída: nenhum problema encontrado.")


if __name__ == "__main__":
    executar_auditoria()
