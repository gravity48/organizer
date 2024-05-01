REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DATE_FORMAT': '%d.%m.%Y',
    'DATE_INPUT_FORMATS': ['%d.%m.%Y'],
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
    ],
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'Organizer API',
    'DESCRIPTION': 'Organizer backend service',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
