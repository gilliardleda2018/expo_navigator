# Expo Navigator — Guia de Veneza

Aplicativo Streamlit para comunicação em italiano durante deslocamentos em Veneza.

## Funcionalidades
- 12 perguntas essenciais para aeroporto, transporte aquático, hospedagem e segurança.
- Reprodução da pergunta em italiano por voz (quando OPENAI_API_KEY está configurada).
- Captura de resposta pelo microfone com controle único, sem botão de parada ocioso.
- Transcrição automática em italiano após o encerramento da gravação pelo widget do navegador.
- Tradução para português e áudio da tradução.
- Mensagens explícitas de erro e possibilidade de editar o texto transcrito.

## Execução
```bash
pip install -r requirements.txt
export OPENAI_API_KEY="sua-chave"
streamlit run app.py
```

Também é possível configurar a chave via `.streamlit/secrets.toml` (não versionar).

**Atenção:** a transcrição e a síntese de voz exigem credenciais válidas, rede e permissão de microfone. O widget `st.audio_input` apresenta o controle nativo de iniciar/parar durante a captura; o aplicativo não mostra controles extras de parada quando ocioso. Não há deploy automático configurado.
