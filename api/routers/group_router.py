from typing import List

from fastapi import APIRouter, Depends

from api.dependencies.deps_utils.utils import get_current_user
from api.dependencies.entity_finder import get_entity_by_id
from api.services.group_service import GroupService
from core.models import Group, User
from core.schemas.group import GroupRead, GroupCreate

router = APIRouter(
    prefix="/groups",
    tags=["Group"],
)


@router.get("",
            response_model=List[GroupRead],
            summary="Get all groups", )
async def get_all_groups(
        limit: int = 10,
        offset: int = 0,
        service: GroupService = Depends()
):
    groups = await service.get_all_groups(offset=offset, limit=limit)
    return groups


@router.get('/{group_id}',
            dependencies=[Depends(get_entity_by_id(Group, 'group_id'))],
            summary='Get group by it\'s id')
async def read_group_by_id(
        group_id: int,
        service: GroupService = Depends()

):
    group = await service.get_group_by_id(group_id)
    return group


@router.post('',
             response_model=GroupRead,
             summary='Add group to database')
async def add_group(
        group: GroupCreate,
        service: GroupService = Depends()
):
    group = service.create_group(group=group)
    return await group

@router.post('/add_user_to_group/{group_id}/{user_id}',
             dependencies=[Depends(get_entity_by_id(Group, 'group_id')),
                           Depends(get_entity_by_id(User, 'user_id'))],
             summary='Add user to group')
async def add_user_to_group(
        group_id: int,
        user_id: int,
        service: GroupService = Depends(),
        current_user: User = Depends(get_current_user)
):
    return await service.add_user_to_group(group_id=group_id, user_id=user_id, current_user=current_user)


@router.put('/{group_id}',
            dependencies=[Depends(get_entity_by_id(Group, 'group_id'))],
            response_model=GroupRead,
            summary='Update group by it\'s id')
async def update_group(
        group_id: int,
        group: GroupCreate,
        service: GroupService = Depends(),
        current_user: User = Depends(get_current_user)
):
    group = service.update_group(group_id=group_id, group=group, current_user=current_user)
    return await group


@router.delete('/{group_id}',
               dependencies=[Depends(get_entity_by_id(Group, 'group_id'))],
               response_model=GroupRead,
               summary='Get group by it\'s id')
async def delete_group(
        group_id: int,
        service: GroupService = Depends(),
        current_user: User = Depends(get_current_user)
):
    group = await service.delete_group_by_id(group_id=group_id, current_user=current_user)
    return group

@router.delete('/delete_user_from_group/{group_id}/{user_id}',
               dependencies=[Depends(get_entity_by_id(Group, 'group_id')),
                             Depends(get_entity_by_id(User, 'user_id'))],
               summary='Add user to group')
async def delete_user_from_group(
        group_id: int,
        user_id: int,
        service: GroupService = Depends(),
        current_user: User = Depends(get_current_user)
):
    return await service.delete_user_from_group(group_id=group_id, user_id=user_id, current_user=current_user)
