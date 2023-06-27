from flask import Flask, request
import requests
import re
import os

app = Flask(__name__)

KEYCLOAK_URL = os.getenv('KEYCLOAK_URL', 'http://keycloak:8080')
KEYCLOAK_USERNAME = os.getenv('KEYCLOAK_USERNAME', 'admin')
KEYCLOAK_PASSWORD = os.getenv('KEYCLOAK_PASSWORD', 'admin')

def get_admin_token():
    data = {
        "username": KEYCLOAK_USERNAME,
        "password": KEYCLOAK_PASSWORD,
        "grant_type": "password",
        "client_id": "admin-cli",
    }
    response = requests.post(f"{KEYCLOAK_URL}/auth/realms/master/protocol/openid-connect/token", data=data)
    response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx
    return response.json()["access_token"]

@app.route('/create-realm', methods=['POST'])
def create_realm():
    realm_name = request.json.get('realm_name')
    password_policy = request.json.get('password_policy')
    if not realm_name or not re.match("^[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*$", realm_name):
        return {"error": "Invalid realm name. It should be a valid DNS subdomain."}, 400

    admin_token = get_admin_token()

    # Create realm with password policy
    headers = {"Authorization": f"Bearer {admin_token}"}
    data = {
        "realm": realm_name,
        "passwordPolicy": password_policy,
        "enabled": True,
    }
    response = requests.post(f"{KEYCLOAK_URL}/auth/admin/realms", headers=headers, json=data)
    if response.status_code != 201:
        return {"error": "Failed to create realm."}, 500

    return {"success": "Realm created successfully."}, 201

@app.route('/list-realms', methods=['GET'])
def list_realms():
    admin_token = get_admin_token()

    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.get(f"{KEYCLOAK_URL}/auth/admin/realms", headers=headers)
    response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx
    realms = response.json()

    # Convert list of realms to a dictionary where the keys are the realm names
    return {"realms": {realm['realm']: realm for realm in realms}}, 200

@app.route('/enforce-policy', methods=['PUT'])
def enforce_policy():
    new_password_policy = request.json.get('password_policy')
    if not new_password_policy:
        return {"error": "No password policy provided."}, 400

    admin_token = get_admin_token()
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Fetch all the realms
    response = requests.get(f"{KEYCLOAK_URL}/auth/admin/realms", headers=headers)
    response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx
    realms = response.json()

    # Update each realm with the new password policy
    for realm in realms:
        realm_name = realm['realm']
        update_password_policy(realm_name, new_password_policy, admin_token)

    return {"success": "Password policy enforced successfully."}, 200


def update_password_policy(realm_name, new_password_policy, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    data = {"passwordPolicy": new_password_policy}
    response = requests.put(f"{KEYCLOAK_URL}/auth/admin/realms/{realm_name}", headers=headers, json=data)
    response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx
