from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_get_all_groups_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/groups",
        headers={'Authorization': f'Bearer {token}'})

    groups = response.json()

    assert response.status_code == 200
    assert len(groups) == 2


async def test_get_all_groups_401(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    response = await async_client.get(
        "/api/groups")

    assert response.status_code == 401


async def test_get_group_by_id_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/groups/1",
        headers={'Authorization': f'Bearer {token}'})

    group = response.json()

    assert response.status_code == 200
    assert group['id'] == 1


async def test_get_group_by_id_401(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    response = await async_client.get(
        "/api/groups/1")

    assert response.status_code == 401


async def test_get_group_by_id_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/groups/10",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_add_group_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.post(
        "/api/groups",
        json={
            'name': 'TestGroup3',
            'creator_id': 1
        },
        headers={'Authorization': f'Bearer {token}'})

    group = response.json()

    assert response.status_code == 200
    assert group['id'] == 3
    assert group['name'] == "TestGroup3"


async def test_add_group_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.post(
        "/api/groups",
        json={
            'name': 'TestGroup3',
            'creator_id': 1
        })

    assert response.status_code == 401


async def test_update_group_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.put(
        "/api/groups/1",
        json={
            'name': 'NewTestGroup1',
            'creator_id': 1
        },
        headers={'Authorization': f'Bearer {token}'})

    group = response.json()

    assert response.status_code == 200
    assert group['id'] == 1
    assert group['name'] == "NewTestGroup1"


async def test_update_group_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.put(
        "/api/groups/1",
        json={
            'name': 'NewTestGroup1',
            'creator_id': 1
        }, )

    assert response.status_code == 401


async def test_update_group_403(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('testuser2')

    response = await async_client.put(
        "/api/groups/1",
        json={
            'name': 'NewTestGroup1',
            'creator_id': 1
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 403


async def test_update_group_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.put(
        "/api/groups/10",
        json={
            'name': 'NewTestGroup1',
            'creator_id': 1
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_delete_group_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.delete(
        "/api/groups/1",
        headers={'Authorization': f'Bearer {token}'})

    group = response.json()

    assert response.status_code == 200
    assert group['id'] == 1
    assert group['name'] == "TestGroup1"


async def test_delete_group_401(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    response = await async_client.delete(
        "/api/groups/1")

    assert response.status_code == 401


async def test_delete_group_403(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('testuser2')

    response = await async_client.delete(
        "/api/groups/1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 403


async def test_delete_group_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.delete(
        "/api/groups/10",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_add_user_to_group_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.post(
        "/api/groups/add_user_to_group/1/3",
        headers={'Authorization': f'Bearer {token}'})

    added_user = response.json()

    assert response.status_code == 200
    assert added_user == 'User 3 added successfully'


async def test_add_user_to_group_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.post(
        "/api/groups/add_user_to_group/1/3")

    assert response.status_code == 401


async def test_add_user_to_group_403(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('testuser2')

    response = await async_client.post(
        "/api/groups/add_user_to_group/1/3",
        headers={'Authorization': f'Bearer {token}'})

    added_user = response.json()

    assert response.status_code == 403
    assert added_user['detail'] == 'Only group owners can add users to chat'


async def test_add_user_to_group_no_user_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.post(
        "/api/groups/add_user_to_group/1/10",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_add_user_to_group_no_group_404(async_client: AsyncClient, async_db: AsyncSession,
                                              get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.post(
        "/api/groups/add_user_to_group/10/1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_add_user_to_group_409(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.post(
        "/api/groups/add_user_to_group/1/2",
        headers={'Authorization': f'Bearer {token}'})

    added_user = response.json()

    assert response.status_code == 409
    assert added_user['detail'] == "User already exists in this group"


async def test_delete_user_from_group_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.delete(
        "/api/groups/delete_user_from_group/1/2",
        headers={'Authorization': f'Bearer {token}'})

    deleted_user = response.json()

    assert response.status_code == 200
    assert deleted_user == 'User deleted from group successfully'


async def test_delete_user_from_group_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.delete(
        "/api/groups/delete_user_from_group/1/2")

    assert response.status_code == 401


async def test_delete_user_from_group_403(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('testuser2')

    response = await async_client.delete(
        "/api/groups/delete_user_from_group/1/1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 403


async def test_delete_user_from_group_no_group_404(async_client: AsyncClient, async_db: AsyncSession,
                                                   get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.delete(
        "/api/groups/delete_user_from_group/10/2",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_delete_user_from_group_no_user_404(async_client: AsyncClient, async_db: AsyncSession,
                                                  get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.delete(
        "/api/groups/delete_user_from_group/1/3",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404
