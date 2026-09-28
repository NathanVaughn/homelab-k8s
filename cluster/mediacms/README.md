# MediaCMS

## Setup

## Bitwarden secrets

- `MEDIACMS_ADMIN_EMAIL`
- `MEDIACMS_ADMIN_PASSWORD`
- `MEDIACMS_ADMIN_USERNAME`
- `MEDIACMS_DB_DATABASE`
- `MEDIACMS_DB_PASSWORD`
- `MEDIACMS_DB_USERNAME`
- `MEDIACMS_SECRET_KEY`
- `MEDIACMS_SMTP_HOST`
- `MEDIACMS_SMTP_PASSWORD`
- `MEDIACMS_SMTP_USERNAME`

## Re-Encode All Media

```python
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms.settings")
import django

django.setup()

from files.models import Media, EncodeProfile

profiles = list(EncodeProfile.objects.filter(active=True))
for media in Media.objects.filter(media_type="video"):
    media.encode(profiles=profiles)
    print(f"Queued encoding for: {media.friendly_token}")
```
