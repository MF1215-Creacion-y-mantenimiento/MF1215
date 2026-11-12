# -*- coding: utf-8 -*-
{
    'name': 'Gestión de eventos de empresa',
    'summary': 'Eventos formativos de empresa e inscripciones de contactos',
    'description': """
Addon del proyecto de la UF1889 (MF1215_3).
Fase 1: estructura, modelo y permisos.
Fase 2: calculados, onchange y restricciones.
Fase 3: análisis funcional y relaciones.
Fase 4: inscripción, validación y errores.
""",
    'author': 'MF1215_3',
    'category': 'Marketing/Events',
    'version': '19.0.1.2.0',
    'license': 'LGPL-3',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/taller_evento_views.xml',
        'views/taller_inscripcion_views.xml',
        'views/menus.xml',
        'data/ir_sequence_data.xml',
        'views/taller_evento_views.xml',
        'views/taller_inscripcion_views.xml',
        'views/taller_exportacion_views.xml',
        'views/gestion_eventos_empresa_menus.xml',
    ],
    'application': True,
    'installable': True,    
}
