"""Temporary launch lock: only the approved, non-indexable GitHub preview."""

PREVIEW_URL = 'https://klartext-digital.github.io/klartext-mint/'


def validate_preview(config):
    """Fail closed before building or publishing; launch requires a new decision."""
    if config.get('base_url') != PREVIEW_URL:
        raise ValueError('Publication paused for other domains. Only the approved GitHub preview is allowed.')
    if config.get('indexable') is not False or config.get('approved_paths') != []:
        raise ValueError('The preview must remain noindex with no approved indexable paths.')
