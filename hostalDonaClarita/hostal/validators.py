import re
from django.core.exceptions import ValidationError

def validar_rut(value):
    """
    Valida que el RUT sea chileno y correcto (Módulo 11).
    Formato esperado: XXXXXXXX-Y
    """
    # Limpiar espacios si los hubiera
    value = value.strip()
    
    # 1. Validar formato con Regex inicial
    if not re.match(r'^\d{7,8}-[0-9kK]$', value):
        raise ValidationError('Formato RUT inválido. Debe ser XXXXXXXX-Y (Ej: 12345678-9).')

    # 2. Separar número y dígito verificador
    rut_body, dv_ingresado = value.split('-')
    dv_ingresado = dv_ingresado.upper()
    
    # 3. Calcular dígito verificador esperado
    try:
        rut_numero = int(rut_body)
    except ValueError:
        raise ValidationError('El cuerpo del RUT debe ser numérico.')

    suma = 0
    multiplo = 2
    
    # Algoritmo Módulo 11 (recorrido inverso)
    for d in reversed(str(rut_numero)):
        suma += int(d) * multiplo
        multiplo += 1
        if multiplo == 8:
            multiplo = 2
            
    resto = suma % 11
    resultado = 11 - resto
    
    if resultado == 11:
        dv_esperado = '0'
    elif resultado == 10:
        dv_esperado = 'K'
    else:
        dv_esperado = str(resultado)
        
    # 4. Comparar
    if dv_ingresado != dv_esperado:
        raise ValidationError('RUT inválido. El dígito verificador no corresponde.')
