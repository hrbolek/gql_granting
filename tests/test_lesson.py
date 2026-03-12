import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same

default_permissions = {
    "result": [
        {
            "roletype": {
                "id": "b87aed46-dfc3-40f8-ad49-03f4138c7478",
                "name": "studijní administrátor"
            }
        }
    ]
}


async def lesson_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("lessonInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def lesson_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("lessonUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def lesson_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("lessonDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_lesson_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roletype": {"name": "superadmin"}
            }]
        }
    )
    RolePermissionSchemaExtensionOverride.set_response(default_permissions)

    input = {
        "name": "Test Program",
        "topicId": "ef1c48b7-4f65-4696-b89f-a95c2cf8814f"
    }
    result = await lesson_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_lesson_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roletype": {"name": "superadmin"}
            }]
        }
    )
    RolePermissionSchemaExtensionOverride.set_response(default_permissions)


    input = {
        "count": 10,
        "topicId": "ef1c48b7-4f65-4696-b89f-a95c2cf8814f"
    }
    delta = {
        "count": 20,
    }
    result = await lesson_insert(SchemaExecutor, CreateMutation, input)
    lesson_inserted = assert_insert(result)
    payload = {
        **input,
        **lesson_inserted,
        **delta
    }
    result = await lesson_update(SchemaExecutor, CreateMutation, payload)
    lesson_updated = assert_update(result)
    assert_same(delta, lesson_updated)

@pytest.mark.asyncio
async def test_lesson_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roletype": {"name": "superadmin"}
            }]
        }
    )
    RolePermissionSchemaExtensionOverride.set_response(default_permissions)

    input = {
        "name": "Test Lesson",
        "topicId": "ef1c48b7-4f65-4696-b89f-a95c2cf8814f"
    }
    result = await lesson_insert(SchemaExecutor, CreateMutation, input)
    lesson_inserted = assert_insert(result)
    payload = {
        **input,
        **lesson_inserted
    }
    result = await lesson_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)