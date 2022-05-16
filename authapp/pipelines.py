import requests
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode

from django.utils import timezone

from authapp.models import UserProfile
from social_core.exceptions import AuthForbidden


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('http', 'api.vk.com', 'method/users.get', None,
                          urlencode(
                              OrderedDict(fields=','.join(('bdate', 'sex', 'about',
                                                           'has_photo', 'photo_max')),
                                          access_token=response['access_token'],
                                          v=5.131)), None))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return
    data = resp.json()['response'][0]

    data_sex = {
        1: UserProfile.FEMALE,
        2: UserProfile.MALE,
        0: None
    }

    bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
    age = timezone.now().date().year - bdate.year
    if age < 18:
        user.delete()
        raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    user.userprofile.gender = data_sex[data['sex']]

    if data['about']:
        user.userprofile.about = data['about']

    if data['has_photo']:
        photo = data['photo_max']
        photo_response = requests.get(photo)
        if photo_response.status_code == requests.codes.ok:
            path_photo = f'users_avatars/{user.pk}.jpg'
            with open(f'media/{path_photo}', 'wb') as ph:
                ph.write(photo_response.content)
            user.image = path_photo

    user.age = age
    user.save()
