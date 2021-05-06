from drf_project.settings import SITE_URL


def build_url(scheme, uid, token, path):
    """build url to send it in email"""
    return f"{scheme}://{SITE_URL}{path}?token={uid}.{token}"
