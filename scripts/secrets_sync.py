import base64
import os

import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class GitHubSecretManager:
    def __init__(self, github_token, environment):
        self.github_token = github_token
        self.environment = environment
        self.base_url = f'https://api.github.com/repos/Hunter71/quadrocopter'
        self.env_secrets_url = f'{self.base_url}/environments'
        self.repo_secrets_url = f'{self.base_url}/actions/secrets'
        self.public_key_url = f'{self.base_url}/actions/secrets/public-key'
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def get_environment_secrets(self):
        url = f'{self.env_secrets_url}/{self.environment}/secrets'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get('secrets', [])

    def encrypt_secret(self, public_key: str, secret_value: str) -> str:
        public_key = RSA.import_key(public_key.encode('utf-8'))
        cipher = PKCS1_OAEP.new(public_key)
        encrypted = cipher.encrypt(secret_value.encode('utf-8'))
        return base64.b64encode(encrypted).decode('utf-8')

    def create_or_update_repo_secret(self, secret_name, encrypted_value, public_key_id):
        url = f'{self.repo_secrets_url}/{secret_name}'
        data = {
            'encrypted_value': encrypted_value,
            'key_id': public_key_id,
        }
        response = requests.put(url, headers=self.headers, json=data)
        response.raise_for_status()

    def get_public_key(self):
        response = requests.get(self.public_key_url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def sync_secrets(self):
        public_key_info = self.get_public_key()
        public_key_id = public_key_info['key_id']
        public_key = public_key_info['key']
        for secret in self.get_environment_secrets():
            secret_name = f"{secret['name']}_{self.environment.upper()}"
            if secret_value := os.getenv(secret["name"]):
                # encrypted_value = self.encrypt_secret(public_key, secret_value)
                # self.create_or_update_repo_secret(secret_name, encrypted_value, public_key_id)
                print(secret_name, secret_value)
                assert secret_value == f"{self.environment}-{secret['name'].lower().replace("_", "-")}"

if __name__ == '__main__':
    github_token = os.getenv('GITHUB_TOKEN')
    environment = os.getenv('ENVIRONMENT')
    syncer = GitHubSecretManager(github_token, environment)
    syncer.sync_secrets()
