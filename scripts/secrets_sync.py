import base64
import os

import requests
import nacl.encoding
import nacl.public

# Set your GitHub token and repository details
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
ENVIRONMENT = os.getenv('ENVIRONMENT')

# GitHub API URLs
BASE_URL = f'https://api.github.com/repos/Hunter71/quadrocopter'
ENV_SECRETS_URL = f'{BASE_URL}/environments'
REPO_SECRETS_URL = f'{BASE_URL}/actions/secrets'
PUBLIC_KEY_URL = f'{BASE_URL}/actions/secrets/public-key'


# Headers for authentication
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_environment_secrets(environment):
    url = f'{ENV_SECRETS_URL}/{environment}/secrets'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get('secrets', [])

def encrypt_secret(public_key: str, secret_value: str) -> str:
    public_key = nacl.public.PublicKey(public_key.encode("utf-8"), nacl.encoding.Base64Encoder())
    sealed_box = nacl.public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")

def create_or_update_repo_secret(secret_name, encrypted_value, public_key_id):
    url = f'{REPO_SECRETS_URL}/{secret_name}'
    data = {
        'encrypted_value': encrypted_value,
        'key_id': public_key_id,
    }
    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()

def get_public_key():
    response = requests.get(PUBLIC_KEY_URL, headers=headers)
    response.raise_for_status()
    return response.json()

def sync_secrets(public_key_id, public_key):
    for secret in get_environment_secrets(ENVIRONMENT):
        secret_name = f"{secret['name']}_{ENVIRONMENT.upper()}"
        if secret_value := os.getenv(secret["name"]):
            print(secret_name, secret_value)
            assert secret_value == "foo-app-id"
        # encrypted_value = encrypt_secret(public_key, secret_value)
        # create_or_update_repo_secret(secret_name, encrypted_value, public_key_id)

if __name__ == '__main__':
    public_key_info = get_public_key()
    sync_secrets(public_key_info['key_id'], public_key_info['key'])
