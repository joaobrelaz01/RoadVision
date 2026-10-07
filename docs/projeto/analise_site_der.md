# Análise Técnica - Site Câmeras DER/SP

---

**URL:** `http://200.144.30.103:8084`

## 1. Mapeamento & Carregamento

- **Quantidade de Câmeras:** 11 câmeras ativas identificadas na listagem.
- **Disponibilização:**
  - [X] Renderização direta no HTML / API interna
- **Mecanismo:** Carregamento dinâmico via JS/AJAX ao interagir com o filtro ou selecionar um item da lista.

---

## 2. Seletores Principais (Playwright)

| Elemento                    | Seletor (Playwright)                                          | Fallback (XPath/Class)          |
| :-------------------------- | :------------------------------------------------------------ | :------------------------------ |
| **Campo de Busca**    | `page.getByPlaceholder('...')` / `page.locator('#busca')` | `//input[@type='text']`       |
| **Lista de Câmeras** | `page.locator('.camera-item')` / `select`                 | `//select/option`             |
| **Player de Vídeo**  | `page.locator('#video-player')` / `img#stream`            | `//div[@id='player']//iframe` |

---

## 3. Origem do Vídeo / Stream

- **Tipo de Stream:**
  - [X] MJPEG / HLS / Frame dinâmico (validado via DevTools)
- **URL Padrão do Stream:** Formatado conforme requisição interceptada no carregamento do player.

---

## 4. Checklist de Testes

- [X] Validar se o IP/URL responde no ambiente local (`200 OK`).
- [X] Testar busca e seleção de câmera via Playwright Inspector.
- [X] Confirmar se o evento de clique dispara o carregamento do stream.
- [X] Confirmar total de câmeras disponíveis (11 câmeras).
