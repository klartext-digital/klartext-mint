"""Launch lock: by default only the approved, non-indexable GitHub preview.

The production launch is prepared but stays locked. It opens only when
seo.config.json carries "launch_approved": true (exactly the boolean), which
is set solely on the client's explicit order "Livegang" (see docs/LIVEGANG.md).
Complete company data alone never opens the lock.
"""

PREVIEW_URL = 'https://klartext-digital.github.io/klartext-mint/'
PRODUCTION_URL = 'https://klartext-digital.ch/'
PRODUCTION_DOMAIN = 'klartext-digital.ch'


def is_launch(config):
    return config.get('launch_approved') is True


def site_url(config):
    return PRODUCTION_URL if is_launch(config) else PREVIEW_URL


def validate_preview(config):
    """Fail closed before building, checking or publishing."""
    if is_launch(config):
        if config.get('base_url') != PRODUCTION_URL:
            raise ValueError('Launch approved, but base_url is not the production domain.')
        approved = config.get('approved_paths')
        if config.get('indexable') is not True or not isinstance(approved, list) or not approved:
            raise ValueError('Launch approved, but indexing or the approved path list is not set.')
        return
    if config.get('base_url') != PREVIEW_URL:
        raise ValueError('Publication paused for other domains. Only the approved GitHub preview is allowed.')
    if config.get('indexable') is not False or config.get('approved_paths') != []:
        raise ValueError('The preview must remain noindex with no approved indexable paths.')
