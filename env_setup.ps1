# Execute este script no PowerShell para definir variáveis de ambiente para a sessão atual.
# Uso (na pasta do projeto):
# .\env_setup.ps1

# Gera uma SECRET_KEY segura usando Python se disponível, caso contrário usa uma chave fixa temporária.
try {
    $py = python - <<'PY'
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
PY
    if ($LASTEXITCODE -eq 0 -and $py) {
        $env:DJANGO_SECRET_KEY = $py.Trim()
    } else {
        $env:DJANGO_SECRET_KEY = '8r#y!b2@xqzv4s9p7m&k1h6c0tufg5jnw3lao+e^d%r7pzq'
    }
} catch {
    $env:DJANGO_SECRET_KEY = '8r#y!b2@xqzv4s9p7m&k1h6c0tufg5jnw3lao+e^d%r7pzq'
}

# Habilita DEBUG para desenvolvimento local
$env:DJANGO_DEBUG = 'True'

Write-Host "DJANGO_SECRET_KEY definida para a sessão atual (não persistida)."
Write-Host "DJANGO_DEBUG=True"
Write-Host "Agora rode: python manage.py runserver"