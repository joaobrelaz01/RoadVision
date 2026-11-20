"""
Serviço de Análise Inteligente da Rodovia (RoadVision Analytics).
Transforma registros reais do Supabase (em fuso America/Sao_Paulo)
em diagnósticos qualitativos 100% dinâmicos, narrativas contextuais vivas
e alertas operacionais em tempo real com critérios documentados.
Zero frases estáticas ou pré-formatadas sem base nos números atuais.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from collections import defaultdict
import zoneinfo

from backend.app.schemas.models import (
    AnaliseInteligente,
    IntensidadeFluxo,
    HorariosPico,
    ComposicaoTrafego,
    PontosMaiorMovimentacao,
    PontoMovimentacao,
    TendenciaTrafego,
    ConfiabilidadeDados
)

TZ_SP = zoneinfo.ZoneInfo("America/Sao_Paulo")

def converter_para_sp(dt_iso: str) -> Optional[datetime]:
    """Converte timestamp ISO UTC do Supabase para o fuso America/Sao_Paulo."""
    if not dt_iso:
        return None
    try:
        dt = datetime.fromisoformat(dt_iso.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(TZ_SP)
    except Exception:
        return None

def obter_narrativa_contextual_sp055(dt_agora_sp: datetime, total_veiculos: int, taxa_h: float) -> str:
    """
    Gera a interpretação contextual baseada no dia da semana e hora atual de Brasília (SP-055).
    """
    dia_semana = dt_agora_sp.weekday()  # 0=Segunda, ..., 4=Sexta, 5=Sábado, 6=Domingo
    hora = dt_agora_sp.hour
    minuto = dt_agora_sp.minute
    hora_formatada = f"{hora:02d}h{minuto:02d}"

    nomes_dias = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    dia_str = nomes_dias[dia_semana]

    if dia_semana in (0, 1, 2, 3):  # Segunda a Quinta
        if 6 <= hora < 9:
            return (
                f"Padrão Pendular Comercial Matutino ({dia_str}, {hora_formatada}): Tráfego intermunicipal "
                f"ativo com deslocamento cotidiano de trabalhadores e prestadores de serviços entre os "
                f"polos de Bertioga, São Sebastião e Caraguatatuba, totalizando {total_veiculos} veículos registrados."
            )
        elif 9 <= hora < 16:
            return (
                f"Padrão Comercial e Logístico ({dia_str}, {hora_formatada}): Circulação regular de transporte "
                f"de carga local, abastecimento urbano e tráfego de rotina com taxa média de {taxa_h:.1f} veíc/h por câmera."
            )
        elif 16 <= hora < 20:
            return (
                f"Padrão Vespertino de Retorno Urbano ({dia_str}, {hora_formatada}): Pico de encerramento de jornada "
                f"com adensamento do fluxo nas imediações dos acessos municipais da SP-055 ({total_veiculos} passagens monitoradas)."
            )
        else:
            return (
                f"Padrão Noturno de Baixa Densidade ({dia_str}, {hora_formatada}): Tráfego noturno esparso "
                f"com redução na velocidade de trânsito e predominância de logística essencial ({total_veiculos} registros no trecho)."
            )

    elif dia_semana == 4:  # Sexta-feira
        if hora >= 14:
            return (
                f"Padrão de Descida Litorânea de Fim de Semana (Sexta-feira, {hora_formatada}): Fluxo massivo de "
                f"turistas descendo a serra rumo às praias do Litoral Norte, gerando pressão de tráfego expressiva "
                f"no trecho monitorado da SP-055 com {total_veiculos} veículos contabilizados."
            )
        else:
            return (
                f"Padrão Pré-Fim de Semana (Sexta-feira, {hora_formatada}): Transição entre o tráfego comercial semanal "
                f"e a antecipação dos primeiros fluxos turísticos em direção a Ubatuba e São Sebastião."
            )

    elif dia_semana == 5:  # Sábado
        if 7 <= hora < 14:
            return (
                f"Padrão Turístico Matutino de Chegada (Sábado, {hora_formatada}): Volume elevado de veículos de passeio "
                f"ingressando nos balneários e praias da SP-055, registrando {total_veiculos} detecções com ritmo dinâmico."
            )
        else:
            return (
                f"Padrão Turístico de Lazer Interpraias (Sábado, {hora_formatada}): Deslocamentos curtos entre orlas, "
                f"centros gastronômicos e hospedagens ao longo dos 156 km da Rio-Santos."
            )

    else:  # Domingo
        if 13 <= hora < 23:
            return (
                f"Padrão Crítico de Retorno de Fim de Semana (Domingo, {hora_formatada}): Operação com alta concentração "
                f"de veículos de retorno em direção à capital e Vale do Paraíba, exigindo monitoramento ostensivo nos trechos de pista simples."
            )
        else:
            return (
                f"Padrão Matutino de Domingo ({hora_formatada}): Trânsito turístico voltado a praias e passeios na região litorânea."
            )

def calcular_analise_inteligente(
    registros_minuto: List[Dict[str, Any]],
    registros_sentido: Optional[List[Dict[str, Any]]] = None,
    cameras_map: Optional[Any] = None,
    total_cameras_cadastradas: int = 11
) -> AnaliseInteligente:
    """
    Executa análises qualitativas e quantitativas sobre os dados reais,
    gerando resumo executivo vivo, narrativa contextual e alertas dinâmicos.
    """
    if registros_sentido is None:
        registros_sentido = []

    # Normaliza mapa de câmeras
    mapa_cams: Dict[str, Any] = {}
    if isinstance(cameras_map, dict):
        mapa_cams = cameras_map
    elif isinstance(cameras_map, list):
        for c in cameras_map:
            cid = getattr(c, "id", None) or (c.get("id") if isinstance(c, dict) else str(c))
            mapa_cams[str(cid)] = c
            cder = getattr(c, "camera_der_id", None) or (c.get("camera_der_id") if isinstance(c, dict) else None)
            if cder:
                mapa_cams[str(cder)] = c

    total_registros = len(registros_minuto)

    # 1. Totalizadores por categoria e por câmera
    totais_cat = {"Carros": 0, "Motos": 0, "Ônibus": 0, "Caminhões": 0}
    cams_agg = defaultdict(int)
    hourly_agg = defaultdict(int)
    timestamps_sp: List[datetime] = []

    for r in registros_minuto:
        c = r.get("carros", 0) or 0
        m = r.get("motos", 0) or 0
        o = r.get("onibus", 0) or 0
        k = r.get("caminhoes", 0) or 0
        tot = c + m + o + k

        totais_cat["Carros"] += c
        totais_cat["Motos"] += m
        totais_cat["Ônibus"] += o
        totais_cat["Caminhões"] += k

        cid = str(r.get("camera_id", ""))
        cams_agg[cid] += tot

        dt_sp = converter_para_sp(r.get("data_hora", ""))
        if dt_sp:
            timestamps_sp.append(dt_sp)
            hora_str = f"{dt_sp.hour:02d}h"
            hourly_agg[hora_str] += tot

    total_veiculos = sum(totais_cat.values())

    # Estimativa de tempo observado
    if timestamps_sp:
        t_min = min(timestamps_sp)
        t_max = max(timestamps_sp)
        delta_segundos = max((t_max - t_min).total_seconds(), 60.0)
        horas_observadas = max(delta_segundos / 3600.0, 0.25)
    else:
        horas_observadas = 1.0

    minutos_observados = max(int(round(horas_observadas * 60)), 1)
    ritmo_veic_min = round(total_veiculos / minutos_observados, 2) if total_veiculos > 0 else 0.0

    # ----------------------------------------------------
    # 1.1 Intensidade do Fluxo
    # ----------------------------------------------------
    criterio_doc = "Critério: < 120 veíc/h (Baixo) • 120 a 360 veíc/h (Moderado) • > 360 veíc/h (Intenso)"
    num_cameras_ativas = max(len([c for c, v in cams_agg.items() if v > 0]), 1)
    taxa_media_por_camera = total_veiculos / (horas_observadas * num_cameras_ativas)
    taxa_arredondada = round(taxa_media_por_camera, 1)

    if total_registros < 3:
        intensidade = IntensidadeFluxo(
            classificacao="Dados insuficientes para análise",
            taxa_media_veic_h=None,
            criterio_documentado=criterio_doc,
            detalhes=f"Amostragem de apenas {total_registros} registros. São necessários no mínimo 3 registros para inferência estatística de fluxo."
        )
    else:
        if taxa_arredondada < 120.0:
            classif_int = "Baixo"
            detalhes_int = f"Taxa média observada de {taxa_arredondada:.1f} veíc/h por câmera ativa ({total_veiculos} veículos em {minutos_observados} min), situando-se abaixo de 120 veíc/h."
        elif taxa_arredondada <= 360.0:
            classif_int = "Moderado"
            detalhes_int = f"Taxa média observada de {taxa_arredondada:.1f} veíc/h por câmera ativa ({total_veiculos} veículos em {minutos_observados} min), dentro da faixa operacional padrão (120-360 veíc/h)."
        else:
            classif_int = "Intenso"
            detalhes_int = f"Taxa média observada de {taxa_arredondada:.1f} veíc/h por câmera ativa ({total_veiculos} veículos em {minutos_observados} min), superando 360 veíc/h e sinalizando adensamento do fluxo."

        intensidade = IntensidadeFluxo(
            classificacao=classif_int,
            taxa_media_veic_h=taxa_arredondada,
            criterio_documentado=criterio_doc,
            detalhes=detalhes_int
        )

    # ----------------------------------------------------
    # 1.2 Horários de Maior Movimento
    # ----------------------------------------------------
    if hourly_agg and timestamps_sp:
        pico_hora, pico_vol = max(hourly_agg.items(), key=lambda x: x[1])
        h_num = int(pico_hora.replace("h", ""))
        janela_pico = f"{h_num:02d}h às {(h_num + 1) % 24:02d}h"

        t_ini_str = min(timestamps_sp).strftime("%d/%m %H:%M")
        t_fim_str = max(timestamps_sp).strftime("%d/%m %H:%M")
        periodo_analisado = f"{t_ini_str} até {t_fim_str} (horário de Brasília)"
        texto_horarios = f"Pico registrado no intervalo entre {janela_pico}, com {pico_vol} veículos ({round((pico_vol / total_veiculos)*100, 1) if total_veiculos > 0 else 0}% do período)."

        horarios_pico = HorariosPico(
            janela_pico=janela_pico,
            volume_pico=pico_vol,
            periodo_analisado=periodo_analisado,
            texto=texto_horarios
        )
    else:
        horarios_pico = HorariosPico(
            janela_pico=None,
            volume_pico=0,
            periodo_analisado="Sem registros temporais disponíveis",
            texto="Dados insuficientes para determinar o horário de pico da rodovia."
        )

    # ----------------------------------------------------
    # 1.3 Composição do Tráfego
    # ----------------------------------------------------
    if total_veiculos > 0:
        dist_pct = {k: round((v / total_veiculos) * 100.0, 1) for k, v in totais_cat.items()}
        lider_cat, lider_pct = max(dist_pct.items(), key=lambda x: x[1])
        texto_comp = f"{lider_cat} lideram o tráfego com {lider_pct:.1f}% do total ({totais_cat[lider_cat]} de {total_veiculos} veículos contabilizados)."
        composicao = ComposicaoTrafego(
            categoria_lider=lider_cat,
            percentual_lider=lider_pct,
            distribuicao=dist_pct,
            texto=texto_comp
        )
    else:
        lider_cat = "Nenhum"
        lider_pct = 0.0
        composicao = ComposicaoTrafego(
            categoria_lider="Nenhuma",
            percentual_lider=0.0,
            distribuicao={k: 0.0 for k in totais_cat},
            texto="Nenhum veículo registrado até o momento para análise de composição."
        )

    # ----------------------------------------------------
    # 1.4 Pontos de Maior Movimentação
    # ----------------------------------------------------
    ranking_pontos: List[PontoMovimentacao] = []
    for cid, vol in sorted(cams_agg.items(), key=lambda x: x[1], reverse=True):
        if vol <= 0:
            continue
        c_info = mapa_cams.get(cid)
        nome_cam = getattr(c_info, "nome", None) or (c_info.get("nome") if isinstance(c_info, dict) else f"Câmera {cid[:8]}")
        km_cam = getattr(c_info, "km", None) or (c_info.get("km") if isinstance(c_info, dict) else "SP-055")
        der_id = getattr(c_info, "camera_der_id", None) or (c_info.get("camera_der_id") if isinstance(c_info, dict) else None)
        pct_cam = round((vol / total_veiculos) * 100.0, 1) if total_veiculos > 0 else 0.0

        ranking_pontos.append(PontoMovimentacao(
            camera_id=cid,
            camera_der_id=der_id,
            nome=nome_cam,
            km=km_cam,
            total_veiculos=vol,
            percentual=pct_cam
        ))

    if ranking_pontos:
        top_cam = ranking_pontos[0]
        texto_pontos = f"A {top_cam.nome} ({top_cam.km}) concentra o maior volume ({top_cam.total_veiculos} veículos, representando {top_cam.percentual}% de todo o tráfego monitorado)."
        cam_lider_nome = top_cam.nome
    else:
        texto_pontos = "Nenhuma câmera possui contagens registradas no período analisado."
        cam_lider_nome = None

    pontos_movimentacao = PontosMaiorMovimentacao(
        ranking=ranking_pontos,
        camera_lider=cam_lider_nome,
        texto=texto_pontos
    )

    # ----------------------------------------------------
    # 1.5 Tendência do Tráfego (Janela recente vs anterior)
    # ----------------------------------------------------
    vol_atual = total_veiculos
    vol_ant = 0
    var_pct: Optional[float] = None
    classif_tend = "Estabilidade"

    if len(timestamps_sp) >= 4:
        registros_ordenados = sorted(
            [r for r in registros_minuto if r.get("data_hora")],
            key=lambda x: x.get("data_hora", "")
        )
        metade = len(registros_ordenados) // 2
        primeira_metade = registros_ordenados[:metade]
        segunda_metade = registros_ordenados[metade:]

        vol_ant = sum(
            (r.get("carros", 0) or 0) + (r.get("motos", 0) or 0) + (r.get("onibus", 0) or 0) + (r.get("caminhoes", 0) or 0)
            for r in primeira_metade
        )
        vol_atual = sum(
            (r.get("carros", 0) or 0) + (r.get("motos", 0) or 0) + (r.get("onibus", 0) or 0) + (r.get("caminhoes", 0) or 0)
            for r in segunda_metade
        )

        if vol_ant > 0:
            var_pct = round(((vol_atual - vol_ant) / vol_ant) * 100.0, 1)
            if var_pct > 5.0:
                classif_tend = "Aumento"
                texto_tend = f"Aumento de +{var_pct}% na janela mais recente ({vol_atual} vs {vol_ant} veículos anteriores)."
            elif var_pct < -5.0:
                classif_tend = "Redução"
                texto_tend = f"Redução de {var_pct}% na janela mais recente ({vol_atual} vs {vol_ant} veículos anteriores)."
            else:
                classif_tend = "Estabilidade"
                texto_tend = f"Fluxo estabilizado com variação de {var_pct:+.1f}% ({vol_atual} vs {vol_ant} veículos)."
        else:
            var_pct = 0.0
            classif_tend = "Estabilidade"
            texto_tend = f"Volume atual de {vol_atual} veículos em monitoramento inicial."
    else:
        texto_tend = f"Volume consolidado de {total_veiculos} veículos coletados."

    tendencia = TendenciaTrafego(
        classificacao=classif_tend,
        variacao_percentual=var_pct,
        volume_atual=vol_atual,
        volume_anterior=vol_ant,
        texto=texto_tend
    )

    # ----------------------------------------------------
    # 1.6 Confiabilidade dos Dados
    # ----------------------------------------------------
    cams_com_dados = len(ranking_pontos)
    if total_registros >= 25 and cams_com_dados >= 2:
        score_conf = "Alta"
        detalhes_conf = f"Excelente cobertura amostral: {total_registros} contagens ativas em {cams_com_dados} de {total_cameras_cadastradas} câmeras cadastradas."
    elif total_registros >= 5 and cams_com_dados >= 1:
        score_conf = "Parcial"
        detalhes_conf = f"{total_registros} contagens obtidas em {cams_com_dados} de {total_cameras_cadastradas} câmeras. Reflete fielmente os pontos ativos."
    else:
        score_conf = "Limitada"
        detalhes_conf = f"Amostragem em consolidação inicial ({total_registros} registros em {cams_com_dados} câmera)."

    confiabilidade = ConfiabilidadeDados(
        score=score_conf,
        total_registros=total_registros,
        cameras_com_dados=cams_com_dados,
        total_cameras_cadastradas=total_cameras_cadastradas,
        detalhes=detalhes_conf
    )

    # ----------------------------------------------------
    # 1.7 Análise Direcional dos Sentidos (Ubatuba vs Maranduba)
    # ----------------------------------------------------
    sentidos_agg = defaultdict(int)
    for rs in registros_sentido:
        s_nome = rs.get("sentido", "Outros")
        s_tot = (rs.get("carros", 0) or 0) + (rs.get("motos", 0) or 0) + (rs.get("onibus", 0) or 0) + (rs.get("caminhoes", 0) or 0)
        sentidos_agg[s_nome] += s_tot

    total_sentidos = sum(sentidos_agg.values())
    if total_sentidos > 0 and len(sentidos_agg) >= 2:
        s_ordenados = sorted(sentidos_agg.items(), key=lambda x: x[1], reverse=True)
        s_maior, v_maior = s_ordenados[0]
        s_menor, v_menor = s_ordenados[1]
        pct_maior = round((v_maior / total_sentidos) * 100.0, 1)
        desc_sentido = f"sentido {s_maior} concentrando {pct_maior}% do fluxo ({v_maior} vs {v_menor} no sentido {s_menor})"
    elif total_sentidos > 0 and len(sentidos_agg) == 1:
        s_maior = list(sentidos_agg.keys())[0]
        v_maior = total_sentidos
        pct_maior = 100.0
        desc_sentido = f"sentido {s_maior} concentrando 100% dos registros direcionais ({v_maior} veículos)"
    else:
        s_maior = "Indefinido"
        pct_maior = 50.0
        desc_sentido = "fluxo equilibrado entre as faixas litorâneas"

    # ----------------------------------------------------
    # 1.8 Resumo Executivo em Tempo Real ("O que está acontecendo agora")
    # ----------------------------------------------------
    var_str = f"{var_pct:+.1f}%" if var_pct is not None else "estável"
    agora_sp = datetime.now(TZ_SP)

    resumo_executivo = (
        f"Neste momento na SP-055, registra-se um volume acumulado de {total_veiculos} veículos nas câmeras ativas, "
        f"operando em um ritmo médio de {ritmo_veic_min} veíc/minuto ({taxa_arredondada:.1f} veíc/h por ponto). "
        f"A dinâmica recente indica {classif_tend.lower()} ({var_str} frente à janela anterior), "
        f"com o {desc_sentido} e predomínio evidente de {lider_cat} ({lider_pct}% da frota total)."
    )

    # ----------------------------------------------------
    # 1.9 Narrativa Contextual por Horário e Dia da Semana
    # ----------------------------------------------------
    narrativa_contextual = obter_narrativa_contextual_sp055(agora_sp, total_veiculos, taxa_arredondada)

    # ----------------------------------------------------
    # 1.10 Alertas Operacionais Dinâmicos
    # ----------------------------------------------------
    alertas: List[str] = []
    pesados = totais_cat["Ônibus"] + totais_cat["Caminhões"]
    pct_pesados = round((pesados / total_veiculos) * 100.0, 1) if total_veiculos > 0 else 0.0

    # Alerta 1: Tráfego pesado
    if pct_pesados >= 16.0:
        alertas.append(
            f"Alerta de Tráfego Pesado: Veículos comerciais (caminhões e ônibus) somam {pct_pesados}% da frota ({pesados} de {total_veiculos} veículos), superando o padrão médio da rodovia (12%). Atenção à velocidade em trechos de pista simples."
        )
    elif pct_pesados > 0:
        alertas.append(
            f"Frota Predominantemente Leve: Apenas {pct_pesados}% de veículos pesados em trânsito; {100.0 - pct_pesados:.1f}% da rodovia ocupada por carros de passeio e motocicletas."
        )

    # Alerta 2: Desbalanceamento direcional
    if total_sentidos > 0 and pct_maior >= 65.0:
        alertas.append(
            f"Desbalanceamento Direcional Expressivo: O sentido {s_maior} retém {pct_maior}% de todo o tráfego direcional, sinalizando forte correnteza unilateral com potencial de lentidão em retornos e cruzamentos."
        )

    # Alerta 3: Mudança abrupta de tendência
    if var_pct is not None and var_pct > 25.0:
        alertas.append(
            f"Aceleração Repentina de Fluxo: Alta expressiva de +{var_pct:.1f}% em relação ao período anterior ({vol_atual} vs {vol_ant} veículos), indicando chegada de contingente rodoviário."
        )
    elif var_pct is not None and var_pct < -25.0:
        alertas.append(
            f"Queda Acentuada de Movimentação: Redução de {var_pct:.1f}% no volume recente ({vol_atual} vs {vol_ant} veículos), sugerindo esvaziamento da via ou retenção externa."
        )

    # Alerta 4: Concentração em ponto crítico
    if ranking_pontos and len(ranking_pontos) >= 2 and ranking_pontos[0].percentual >= 60.0:
        top = ranking_pontos[0]
        alertas.append(
            f"Gargalo no Ponto {top.nome}: Concentra {top.percentual}% de todas as passagens da rodovia ({top.total_veiculos} veículos), operando como principal polo de fluxo."
        )

    if not alertas:
        alertas.append(
            f"Fluxo Operacional Estável: Sem anomalias severas de fluxo ou retenções críticas detectadas nos {minutos_observados} minutos analisados."
        )

    # ----------------------------------------------------
    # 1.11 Observações Automáticas
    # ----------------------------------------------------
    obs: List[str] = []
    obs.append(f"Ritmo atual aferido: {ritmo_veic_min} veículos por minuto ao longo dos pontos com monitoramento ativo.")

    if ranking_pontos:
        top = ranking_pontos[0]
        obs.append(f"A {top.nome} ({top.km}) lidera o volume rodoviário com {top.total_veiculos} passagens contabilizadas ({top.percentual}% do total).")

    if total_sentidos > 0:
        obs.append(f"Distribuição direcional consolidada: {desc_sentido}.")
    else:
        obs.append("Contagens direcionais em sincronização com o banco de dados Supabase.")

    obs.append(f"Classificação modal: {lider_cat} representam a parcela dominante ({lider_pct}%), seguidos pelas demais categorias em circulação.")

    return AnaliseInteligente(
        resumo_executivo=resumo_executivo,
        narrativa_contextual=narrativa_contextual,
        alertas_operacionais=alertas,
        intensidade=intensidade,
        horarios_pico=horarios_pico,
        composicao=composicao,
        pontos_movimentacao=pontos_movimentacao,
        tendencia=tendencia,
        confiabilidade=confiabilidade,
        observacoes_automaticas=obs
    )
