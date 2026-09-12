# MediaCMS

## Setup

```bash
export ADMIN_USER=$ADMIN_USER
export ADMIN_EMAIL=$ADMIN_EMAIL
export ADMIN_PASSWORD=$ADMIN_PASSWORD
export POSTGRES_PASSWORD=$POSTGRES_PASSWORD
export SECRET_KEY=$SECRET_KEY
export EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD
export EMAIL_HOST_USER=$EMAIL_HOST_USER
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n mediacms create secret generic mediacms-env \
--from-literal=ADMIN_USER=$ADMIN_USER \
--from-literal=ADMIN_EMAIL=$ADMIN_EMAIL \
--from-literal=ADMIN_PASSWORD=$ADMIN_PASSWORD \
--from-literal=POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
--from-literal=SECRET_KEY=$SECRET_KEY \
--from-literal=EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD \
--from-literal=EMAIL_HOST_USER=$EMAIL_HOST_USER \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
kubectl delete secret -n mediacms mediacms-env
```

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
