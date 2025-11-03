/* ============================================
   SISTEMA DE GESTIÓN DE HOSTAL - JAVASCRIPT
   ============================================ */

// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    
    /* ============================================
       AUTO-CIERRE DE MENSAJES DEL SISTEMA
       ============================================ */
    initAutoCloseMessages();
    
    /* ============================================
       VALIDACIÓN DE FORMULARIOS
       ============================================ */
    initFormValidation();
    
    /* ============================================
       CONFIRMACIONES DE ELIMINACIÓN
       ============================================ */
    initDeleteConfirmations();
    
    /* ============================================
       VALIDACIÓN DE RUT CHILENO
       ============================================ */
    initRutValidation();
    
    /* ============================================
       PREVIEW DE ARCHIVOS
       ============================================ */
    initFilePreview();
});

/* ============================================
   FUNCIÓN: AUTO-CIERRE DE MENSAJES
   Cierra automáticamente los mensajes después de 5 segundos
   ============================================ */
function initAutoCloseMessages() {
    const messages = document.querySelectorAll('.alert');
    
    messages.forEach(function(message) {
        // Auto cerrar después de 5 segundos
        setTimeout(function() {
            message.style.opacity = '0';
            message.style.transform = 'translateY(-20px)';
            
            // Remover del DOM después de la animación
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
        
        // Botón de cierre manual
        const closeBtn = message.querySelector('.alert-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                message.style.opacity = '0';
                message.style.transform = 'translateY(-20px)';
                setTimeout(function() {
                    message.remove();
                }, 300);
            });
        }
    });
}

/* ============================================
   FUNCIÓN: VALIDACIÓN DE FORMULARIOS
   Valida campos requeridos antes de enviar
   ============================================ */
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(function(field) {
                // Remover clases de error previas
                const formGroup = field.closest('.form-group');
                if (formGroup) {
                    formGroup.classList.remove('has-error');
                }
                
                // Validar campo vacío
                if (!field.value.trim()) {
                    isValid = false;
                    if (formGroup) {
                        formGroup.classList.add('has-error');
                    }
                    
                    // Mostrar mensaje de error si no existe
                    let errorMsg = formGroup.querySelector('.error-message');
                    if (!errorMsg) {
                        errorMsg = document.createElement('span');
                        errorMsg.className = 'error-message';
                        errorMsg.textContent = 'Este campo es obligatorio';
                        formGroup.appendChild(errorMsg);
                    }
                }
            });
            
            // Prevenir envío si hay errores
            if (!isValid) {
                e.preventDefault();
                // Scroll al primer error
                const firstError = form.querySelector('.has-error');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
        
        // Remover error al escribir
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(function(input) {
            input.addEventListener('input', function() {
                const formGroup = this.closest('.form-group');
                if (formGroup) {
                    formGroup.classList.remove('has-error');
                    const errorMsg = formGroup.querySelector('.error-message');
                    if (errorMsg && !errorMsg.dataset.backend) {
                        errorMsg.remove();
                    }
                }
            });
        });
    });
}

/* ============================================
   FUNCIÓN: CONFIRMACIONES DE ELIMINACIÓN
   Muestra diálogo de confirmación antes de eliminar
   ============================================ */
function initDeleteConfirmations() {
    const deleteForms = document.querySelectorAll('form[action*="eliminar"]');
    
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const confirmed = confirm('¿Está seguro de que desea eliminar este registro? Esta acción no se puede deshacer.');
            
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });
    
    // También para botones de eliminación individuales
    const deleteButtons = document.querySelectorAll('.btn-delete[type="submit"]');
    deleteButtons.forEach(function(button) {
        const form = button.closest('form');
        if (form && !form.hasAttribute('data-confirm-added')) {
            form.setAttribute('data-confirm-added', 'true');
            form.addEventListener('submit', function(e) {
                const confirmed = confirm('¿Está seguro de que desea eliminar este registro?');
                if (!confirmed) {
                    e.preventDefault();
                }
            });
        }
    });
}

/* ============================================
   FUNCIÓN: DROPDOWN MENUS
   Maneja la apertura/cierre de menús desplegables
   ============================================ */
function initDropdowns() {
    // Toggle dropdown al hacer click en el botón
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    
    dropdownToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Cerrar otros dropdowns abiertos
            const allDropdowns = document.querySelectorAll('.dropdown-menu.show');
            allDropdowns.forEach(function(menu) {
                if (menu !== toggle.nextElementSibling) {
                    menu.classList.remove('show');
                }
            });
            
            // Toggle el dropdown actual
            const menu = toggle.nextElementSibling;
            if (menu && menu.classList.contains('dropdown-menu')) {
                menu.classList.toggle('show');
            }
        });
    });
    
    // Cerrar dropdown al hacer click fuera
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            const openDropdowns = document.querySelectorAll('.dropdown-menu.show');
            openDropdowns.forEach(function(menu) {
                menu.classList.remove('show');
            });
        }
    });
    
    // Cerrar dropdown al hacer click en una opción
    const dropdownItems = document.querySelectorAll('.dropdown-menu button');
    dropdownItems.forEach(function(item) {
        item.addEventListener('click', function() {
            const menu = this.closest('.dropdown-menu');
            if (menu) {
                menu.classList.remove('show');
            }
        });
    });
}

/* ============================================
   FUNCIÓN: VALIDACIÓN DE RUT CHILENO
   Valida formato y dígito verificador del RUT
   ============================================ */
function initRutValidation() {
    const rutInputs = document.querySelectorAll('input[name="rut"], input[id*="rut"]');
    
    rutInputs.forEach(function(input) {
        // Formatear mientras se escribe
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/[^\dkK-]/g, '');
            e.target.value = value;
        });
        
        // Validar al perder el foco
        input.addEventListener('blur', function(e) {
            const rut = e.target.value;
            const formGroup = e.target.closest('.form-group');
            
            if (rut && !validarRut(rut)) {
                if (formGroup) {
                    formGroup.classList.add('has-error');
                    
                    // Agregar mensaje de error si no existe
                    let errorMsg = formGroup.querySelector('.error-message.rut-error');
                    if (!errorMsg) {
                        errorMsg = document.createElement('span');
                        errorMsg.className = 'error-message rut-error';
                        errorMsg.textContent = 'RUT inválido. Formato: 12345678-9';
                        formGroup.appendChild(errorMsg);
                    }
                }
            } else {
                if (formGroup) {
                    formGroup.classList.remove('has-error');
                    const errorMsg = formGroup.querySelector('.error-message.rut-error');
                    if (errorMsg) {
                        errorMsg.remove();
                    }
                }
            }
        });
    });
}

/* ============================================
   FUNCIÓN AUXILIAR: VALIDAR RUT
   Valida formato y dígito verificador del RUT chileno
   ============================================ */
function validarRut(rut) {
    // Formato: 12345678-9
    const rutPattern = /^(\d{7,8})-([0-9kK])$/;
    
    if (!rutPattern.test(rut)) {
        return false;
    }
    
    const parts = rut.split('-');
    const numero = parts[0];
    const dv = parts[1].toUpperCase();
    
    // Calcular dígito verificador
    let suma = 0;
    let multiplo = 2;
    
    for (let i = numero.length - 1; i >= 0; i--) {
        suma += parseInt(numero.charAt(i)) * multiplo;
        multiplo = multiplo === 7 ? 2 : multiplo + 1;
    }
    
    const dvEsperado = 11 - (suma % 11);
    let dvCalculado;
    
    if (dvEsperado === 11) {
        dvCalculado = '0';
    } else if (dvEsperado === 10) {
        dvCalculado = 'K';
    } else {
        dvCalculado = dvEsperado.toString();
    }
    
    return dv === dvCalculado;
}

/* ============================================
   FUNCIÓN: PREVIEW DE ARCHIVOS
   Muestra el nombre del archivo seleccionado
   ============================================ */
function initFilePreview() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            const formGroup = e.target.closest('.form-group');
            
            if (file && formGroup) {
                // Remover preview anterior
                const oldPreview = formGroup.querySelector('.file-preview');
                if (oldPreview) {
                    oldPreview.remove();
                }
                
                // Crear nuevo preview
                const preview = document.createElement('div');
                preview.className = 'file-preview';
                preview.innerHTML = `
                    <span style="color: #667eea; font-size: 12px; margin-top: 5px; display: block;">
                        📄 Archivo seleccionado: <strong>${file.name}</strong> 
                        (${formatFileSize(file.size)})
                    </span>
                `;
                
                formGroup.appendChild(preview);
            }
        });
    });
}

/* ============================================
   FUNCIÓN AUXILIAR: FORMATEAR TAMAÑO DE ARCHIVO
   Convierte bytes a formato legible
   ============================================ */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/* ============================================
   FUNCIÓN: LOADING SPINNER
   Muestra spinner durante operaciones asíncronas
   ============================================ */
function showLoading(button) {
    const originalText = button.innerHTML;
    button.setAttribute('data-original-text', originalText);
    button.disabled = true;
    button.innerHTML = '<span class="spinner">⏳</span> Procesando...';
    return originalText;
}

function hideLoading(button) {
    const originalText = button.getAttribute('data-original-text');
    if (originalText) {
        button.innerHTML = originalText;
        button.disabled = false;
    }
}

/* ============================================
   FUNCIÓN: FILTROS DINÁMICOS
   Filtra tablas en tiempo real
   ============================================ */
function initTableFilters() {
    const filterInputs = document.querySelectorAll('.table-filter');
    
    filterInputs.forEach(function(input) {
        input.addEventListener('keyup', function(e) {
            const filter = e.target.value.toLowerCase();
            const table = document.querySelector(e.target.getAttribute('data-table'));
            
            if (table) {
                const rows = table.querySelectorAll('tbody tr');
                
                rows.forEach(function(row) {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(filter) ? '' : 'none';
                });
            }
        });
    });
}

/* ============================================
   UTILIDADES EXPORTABLES
   ============================================ */
window.hostalUtils = {
    validarRut: validarRut,
    showLoading: showLoading,
    hideLoading: hideLoading,
    formatFileSize: formatFileSize
};