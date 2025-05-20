from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_get_all_chats_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/chats",
        headers={'Authorization': f'Bearer {token}'})

    chats = response.json()

    assert response.status_code == 200
    assert len(chats) == 2


async def test_get_all_chats_401(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    response = await async_client.get(
        "/api/chats")

    assert response.status_code == 401


async def test_get_chat_by_id_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/chats/1",
        headers={'Authorization': f'Bearer {token}'})

    chat = response.json()

    assert response.status_code == 200
    assert chat['id'] == 1


async def test_get_chat_by_id_401(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    response = await async_client.get(
        "/api/chats/1")

    assert response.status_code == 401


async def test_get_chat_by_id_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/chats/10",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_get_chats_by_group_id_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/chats/get_chat_by_group_id/1",
        headers={'Authorization': f'Bearer {token}'})

    chat = response.json()
    assert response.status_code == 200
    assert chat[0]['id'] == 1


async def test_get_chats_by_group_id_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "/api/chats/get_chat_by_group_id/1")

    assert response.status_code == 401


async def test_get_chats_by_group_id_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/chats/get_chat_by_group_id/10",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_add_chat_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.post(
        "/api/chats",
        json={'name': 'TestChat3',
              'group_id': 1,
              "type": 'private'},
        headers={'Authorization': f'Bearer {token}'})

    chat = response.json()

    assert response.status_code == 200
    assert chat['id'] == 3
    assert chat['name'] == "TestChat3"


async def test_add_chat_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.post(
        "/api/chats",
        json={'name': 'TestChat3',
              'group_id': 1,
              "type": 'private'})

    assert response.status_code == 401


async def test_add_chat_group_not_found_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.post(
        "/api/chats",
        json={'name': 'TestChat3',
              'group_id': 10,
              "type": 'private'},
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_update_chat_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.put(
        "/api/chats/1",
        json={'name': 'NewTestChat1',
              'group_id': 1,
              "type": 'grouped'},
        headers={'Authorization': f'Bearer {token}'})

    chat = response.json()

    assert response.status_code == 200
    assert chat['id'] == 1
    assert chat['name'] == "NewTestChat1"
    assert chat['type'] == "grouped"


async def test_update_chat_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.put(
        "/api/chats/1",
        json={'name': 'NewTestChat1',
              'group_id': 1,
              "type": 'grouped'})

    assert response.status_code == 401


async def test_update_chat_403(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('testuser2')

    response = await async_client.put(
        "/api/chats/1",
        json={'name': 'NewTestChat1',
              'group_id': 1,
              "type": 'grouped'},
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 403


async def test_update_chat_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.put(
        "/api/chats/10",
        json={'name': 'NewTestChat1',
              'group_id': 1,
              "type": 'grouped'},
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_delete_chat_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.delete(
        "/api/chats/1",
        headers={'Authorization': f'Bearer {token}'})

    chat = response.json()

    assert response.status_code == 200
    assert chat['id'] == 1
    assert chat['name'] == "TestChat1"


async def test_delete_chat_401(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    response = await async_client.delete(
        "/api/chats/1")

    assert response.status_code == 401


async def test_delete_chat_403(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('testuser2')

    response = await async_client.delete(
        "/api/chats/1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 403


async def test_delete_chat_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.delete(
        "/api/chats/10",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404

