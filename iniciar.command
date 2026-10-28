#!/bin/bash
set -e
cd "$(dirname "$0")"
if [ ! -x .venv/bin/python ]; then
  echo 'Falta el entorno Python. Sigue README.md para prepararlo.'
  exit 1
fi
mkdir -p .runtime
if ! curl -fsS http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
  if [ -x .local-runtime/Ollama.app/Contents/Resources/ollama ]; then
    OLLAMA_MODELS="$PWD/.local-runtime/models" OLLAMA_HOST=127.0.0.1:11434 OLLAMA_NO_CLOUD=1 .local-runtime/Ollama.app/Contents/Resources/ollama serve >.runtime/ollama.log 2>&1 &
  elif command -v ollama >/dev/null 2>&1; then
    OLLAMA_HOST=127.0.0.1:11434 OLLAMA_NO_CLOUD=1 ollama serve >.runtime/ollama.log 2>&1 &
  else
    echo 'Ollama no está instalado. El informe funciona; el chat necesita Ollama y qwen3:4b-instruct.'
  fi
fi
echo 'Abre http://127.0.0.1:8000 . Ctrl+C detiene la API.'
exec .venv/bin/python -m uvicorn main:app --app-dir 02_backend_y_mcp --host 127.0.0.1 --port 8000
