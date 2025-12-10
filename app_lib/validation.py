from django.core.exceptions import ValidationError
import re

# ============================================================
#   Validador: No permitir números
#   Se usa en campos donde solo deben ir letras.
# ============================================================
def validar_no_numeros(valor):
    # Busca cualquier número en el texto
    if re.search(r'\d', valor):
        raise ValidationError("Este campo no puede contener números.")


# ============================================================
#   Validador: Solo letras, números y espacios
#   Útil para títulos o textos simples.
# ============================================================
def validar_solo_letras_y_num(value):
    # Permite: letras, números, espacios y acentos
    pattern = re.compile(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s]+$')
    if not pattern.match(value):
        raise ValidationError("Solo puede contener letras, números y espacios.")


# ============================================================
#   Validador: Solo letras y espacios
#   Evita números u otros símbolos.
# ============================================================
def validar_solo_letras(value):
    # Permite letras, espacios y acentos
    pattern = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$')
    if not pattern.match(value):
        raise ValidationError("Solo puede contener letras y espacios.")
