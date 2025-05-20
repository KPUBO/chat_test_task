from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_users_me_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/auth/jwt/me",
        headers={'Authorization': f'Bearer {token}'})

    cur_user = response.json()

    assert response.status_code == 200
    assert cur_user['id'] == 1
    assert cur_user['email'] == 'admin@admin.com'

async def test_users_me_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "/api/auth/jwt/me")

    assert response.status_code == 401

async def test_patch_current_user_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.patch(
        "/api/auth/jwt/me",
        json={
            'email': 'newadmin@newadmin.com',
        },
        headers={'Authorization': f'Bearer {token}'})

    cur_user = response.json()

    assert response.status_code == 200
    assert cur_user['id'] == 1
    assert cur_user['email'] == 'newadmin@newadmin.com'


async def test_patch_current_user_422(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.patch(
        "/api/auth/jwt/me",
        json={
            'email': 'new_admin@new_admin.com',
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 422


async def test_patch_current_user_400(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.patch(
        "/api/auth/jwt/me",
        json={
            'email': 'testuser2@testuser2.com',
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 400


async def test_patch_current_user_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.patch(
        "/api/auth/jwt/me",
        json={
            'email': 'testuser2@testuser2.com',
        })

    assert response.status_code == 401


async def test_get_user_by_id_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/users/2",
        headers={'Authorization': f'Bearer {token}'})

    cur_user = response.json()

    assert response.status_code == 200
    assert cur_user['id'] == 2
    assert cur_user['email'] == 'testuser2@testuser2.com'

async def test_get_user_by_id_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "/api/users/2")
    assert response.status_code == 401


async def test_get_user_by_id_403(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('testuser2')

    response = await async_client.get(
        "/api/auth/jwt/2",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 403


async def test_get_user_by_id_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/users/20",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_patch_user_by_id_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.patch(
        "/api/auth/jwt/2",
        json={
            'email': 'newtestuser2@newtestuser2.com',
        },
        headers={'Authorization': f'Bearer {token}'})

    cur_user = response.json()

    assert response.status_code == 200
    assert cur_user['id'] == 2
    assert cur_user['email'] == 'newtestuser2@newtestuser2.com'


async def test_patch_user_by_id_400(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.patch(
        "/api/auth/jwt/1",
        json={
            'email': 'testuser2@testuser2.com',
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 400


async def test_patch_user_by_id_401(async_client: AsyncClient, async_db: AsyncSession) -> None:

    response = await async_client.patch(
        "/api/auth/jwt/2")

    assert response.status_code == 401


async def test_patch_user_by_id_403(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('testuser2')

    response = await async_client.patch(
        "/api/auth/jwt/2",
        json={
            'email': 'newtestuser2@newtestuser2.com',
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 403


async def test_patch_user_by_id_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.patch(
        "/api/auth/jwt/20",
        json={
            'email': 'newtestuser2@newtestuser2.com',
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_patch_user_by_id_422(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.patch(
        "/api/auth/jwt/2",
        json={
            'email': 'newtestuser2@new_testuser2.com',
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 422