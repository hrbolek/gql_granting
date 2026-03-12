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


async def topic_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("topicInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def topic_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("topicUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def topic_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("topicDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_topic_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Topic",
        "semesterId": "49ac365e-c9be-4752-9a46-21542ed361df"
    }
    result = await topic_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_topic_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Topic",
        "nameEn": "Test Topic",
        "semesterId": "49ac365e-c9be-4752-9a46-21542ed361df"
    }
    delta = {
        "name": "Updated Test Topic",
        "nameEn": "Updated Test Topic",
    }
    result = await topic_insert(SchemaExecutor, CreateMutation, input)
    topic_inserted = assert_insert(result)
    payload = {
        **input,
        **topic_inserted,
        **delta
    }
    result = await topic_update(SchemaExecutor, CreateMutation, payload)
    topic_updated = assert_update(result)
    assert_same(delta, topic_updated)

@pytest.mark.asyncio
async def test_topic_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Topic",
        "semesterId": "49ac365e-c9be-4752-9a46-21542ed361df"
    }
    result = await topic_insert(SchemaExecutor, CreateMutation, input)
    topic_inserted = assert_insert(result)
    payload = {
        **input,
        **topic_inserted
    }
    result = await topic_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)