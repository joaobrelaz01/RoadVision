import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from backend.app.main import app

def test_all():
    c = TestClient(app)

    # 1. Dashboard
    r = c.get('/api/dashboard')
    assert r.status_code == 200, f'Dashboard status: {r.status_code}'
    data = r.json()
    print('[OK] /api/dashboard status 200')
    print('     Metrics:', data['metrics']['total_veiculos'], 'veiculos, Extensao:', data['metrics'].get('extensao_trecho_cadastrado_km'), 'km')
    assert 'analise_inteligente' in data
    ai = data['analise_inteligente']
    print('     Intensidade:', ai['intensidade']['classificacao'], f"({ai['intensidade']['taxa_media_veic_h']} veic/h)")
    print('     Pico:', ai['horarios_pico']['janela_pico'])
    print('     Lider:', ai['composicao']['categoria_lider'], f"({ai['composicao']['percentual_lider']}%)")
    print('     Tendencia:', ai['tendencia']['classificacao'])
    print('     Confiabilidade:', ai['confiabilidade']['score'])
    print('     Observacoes:', len(ai['observacoes_automaticas']))

    # 2. Analise inteligente dedicada
    r = c.get('/api/dashboard/analise-inteligente')
    assert r.status_code == 200
    print('[OK] /api/dashboard/analise-inteligente status 200')

    # 3. Cameras
    r = c.get('/api/cameras')
    assert r.status_code == 200
    cams = r.json()
    print('[OK] /api/cameras status 200, count:', len(cams))

    # 4. Ultima captura geral
    r = c.get('/api/cameras/ultima-captura')
    assert r.status_code == 200
    uc = r.json()
    print('[OK] /api/cameras/ultima-captura status 200, origem:', uc['origem'], 'image_url:', uc['image_url'], 'fuso:', uc['captured_at'])

    # 5. Ultima captura por camera (camera 36)
    r = c.get(f"/api/cameras/{cams[0]['id']}/ultima-captura")
    assert r.status_code == 200
    print('[OK] /api/cameras/{cam_id}/ultima-captura status 200')

    # 6. Servir arquivo de captura local
    r = c.get('/api/cameras/capturas/arquivo/camera_36.jpg')
    assert r.status_code == 200 and r.headers['content-type'] == 'image/jpeg'
    print('[OK] /api/cameras/capturas/arquivo/camera_36.jpg status 200, bytes:', len(r.content))

    # 7. Estatisticas
    r = c.get('/api/estatisticas')
    assert r.status_code == 200
    est = r.json()
    print('[OK] /api/estatisticas status 200, total_periodo:', est['total_periodo'])

    # 8. Relatorios
    r = c.get('/api/relatorios')
    assert r.status_code == 200
    rel = r.json()
    print('[OK] /api/relatorios status 200, registros:', rel['total_registros'])

    # 9. Usuarios (com joao como admin)
    r = c.get('/api/auth/usuarios')
    assert r.status_code == 200
    users = r.json()
    joao = next((u for u in users if u['email'] == 'joao.santossilva@uni9.edu.br'), None)
    assert joao is not None
    print('[OK] /api/auth/usuarios status 200, user joao:', joao['nome'], 'cargo:', joao['cargo'])

    # 10. Status do sistema
    r = c.get('/api/status')
    assert r.status_code == 200
    st = r.json()
    print('[OK] /api/status status 200, supabase:', st['supabase_connected'], 'limite_cameras:', st['active_cameras_limit'])
    print('\nTODOS OS ENDPOINTS VALIDADOS COM SUCESSO!')

if __name__ == '__main__':
    test_all()
