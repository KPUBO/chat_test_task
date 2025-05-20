from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_get_all_messages_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/messages",
        headers={'Authorization': f'Bearer {token}'})

    messages = response.json()

    assert response.status_code == 200
    assert len(messages) == 5


async def test_get_all_messages_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "/api/messages")

    assert response.status_code == 401


async def test_get_message_by_id_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/messages/1",
        headers={'Authorization': f'Bearer {token}'})

    message = response.json()

    assert response.status_code == 200
    assert message['id'] == 1


async def test_get_message_by_id_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "/api/messages/1")

    assert response.status_code == 401


async def test_get_message_by_id_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/messages/10",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_get_all_messages_by_chat_id_200(async_client: AsyncClient, async_db: AsyncSession,
                                               get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/messages/get_messages_by_chat_id/1",
        headers={'Authorization': f'Bearer {token}'}
    )

    messages = response.json()

    assert response.status_code == 200
    assert len(messages) == 2


async def test_get_all_messages_by_chat_id_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "/api/messages/get_messages_by_chat_id/1")

    assert response.status_code == 401


async def test_get_all_messages_by_chat_id_404(async_client: AsyncClient, async_db: AsyncSession,
                                               get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/messages/get_messages_by_chat_id/10",
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 404


async def test_create_message_200(async_client: AsyncClient, async_db: AsyncSession,
                                  get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.post(
        "/api/messages",
        headers={'Authorization': f'Bearer {token}'},
        json={
            'chat_id': 1,
            'content': "NewTestMessage1"
        }
    )

    message = response.json()

    assert response.status_code == 200
    assert message['id'] == 6


async def test_create_message_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.post(
        "/api/messages",
        json={
            'chat_id': 1,
            'content': "NewTestMessage1"
        }
    )

    assert response.status_code == 401


async def test_create_message_422(async_client: AsyncClient, async_db: AsyncSession,
                                  get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.post(
        "/api/messages",
        headers={'Authorization': f'Bearer {token}'},
        json={
            'chat_id': 'tst',
            'content': "NewTestMessage1"
        }
    )

    assert response.status_code == 422


async def test_update_message_200(async_client: AsyncClient, async_db: AsyncSession,
                                  get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.put(
        "/api/messages/1",
        headers={'Authorization': f'Bearer {token}'},
        json={
            'chat_id': 1,
            'content': "NewTestMessage1"
        }
    )

    message = response.json()

    assert response.status_code == 200
    assert message['id'] == 1
    assert message['content'] == "NewTestMessage1"


async def test_update_message_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.put(
        "/api/messages/1",
        json={
            'chat_id': 1,
            'content': "NewTestMessage1"
        }
    )

    assert response.status_code == 401


async def test_update_message_404(async_client: AsyncClient, async_db: AsyncSession,
                                  get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.put(
        "/api/messages/10",
        headers={'Authorization': f'Bearer {token}'},
        json={
            'chat_id': 1,
            'content': "NewTestMessage1"
        }
    )

    assert response.status_code == 404


async def test_update_message_422(async_client: AsyncClient, async_db: AsyncSession,
                                  get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.put(
        "/api/messages/1",
        headers={'Authorization': f'Bearer {token}'},
        json={
            'chat_id': 'tst',
            'content': "NewTestMessage1"
        }
    )

    assert response.status_code == 422


async def test_delete_message_200(async_client: AsyncClient, async_db: AsyncSession,
                                  get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.delete(
        "/api/messages/1",
        headers={'Authorization': f'Bearer {token}'}
    )

    message = response.json()

    assert response.status_code == 200
    assert message['id'] == 1
    assert message['content'] == "Test content for chat 1 from user 1"


async def test_delete_message_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.delete(
        "/api/messages/1"
    )

    assert response.status_code == 401


async def test_delete_message_403(async_client: AsyncClient, async_db: AsyncSession,
                                  get_user_token) -> None:
    token = await get_user_token('testuser2')

    response = await async_client.delete(
        "/api/messages/1",
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 403


async def test_delete_message_404(async_client: AsyncClient, async_db: AsyncSession,
                                  get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.delete(
        "/api/messages/10",
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 404


async def test_delete_message_422(async_client: AsyncClient, async_db: AsyncSession,
                                  get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.delete(
        "/api/messages/test",
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 422


async def test_read_message_200(async_client: AsyncClient, async_db: AsyncSession,
                                get_user_token) -> None:
    token = await get_user_token('testuser2')

    response = await async_client.patch(
        "/api/messages/read_message/1",
        headers={'Authorization': f'Bearer {token}'},
    )

    message = response.json()

    assert response.status_code == 200
    assert message['id'] == 1
    assert message['content'] == "Test content for chat 1 from user 1"
    assert message['is_fully_read'] is True


async def test_read_message_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.patch(
        "/api/messages/read_message/1"
    )

    assert response.status_code == 401


async def test_read_message_no_message_404(async_client: AsyncClient, async_db: AsyncSession,
                                           get_user_token) -> None:
    token = await get_user_token('testuser2')

    response = await async_client.patch(
        "/api/messages/read_message/10",
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 404


async def test_read_message_missing_user_404(async_client: AsyncClient, async_db: AsyncSession,
                                             get_user_token) -> None:
    token = await get_user_token('testuser3')

    response = await async_client.patch(
        "/api/messages/read_message/1",
        headers={'Authorization': f'Bearer {token}'},
    )

    message = response.json()

    assert response.status_code == 404
    assert message['detail'] == 'Note not found'
