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


async def evaluation_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("evaluationInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def evaluation_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("evaluationUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def evaluation_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("evaluationDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_evaluation_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Evaluation",
        "subjectId": "3c0f46a2-f7ba-4ae5-9a07-2c21662db562"
    }
    result = await evaluation_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_evaluation_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Evaluation",
        "nameEn": "Test Evaluation",
        "subjectId": "3c0f46a2-f7ba-4ae5-9a07-2c21662db562"
    }
    delta = {
        "name": "Updated Test Evaluation",
        "nameEn": "Updated Test Evaluation",
    }
    result = await evaluation_insert(SchemaExecutor, CreateMutation, input)
    evaluation_inserted = assert_insert(result)
    payload = {
        **input,
        **evaluation_inserted,
        **delta
    }
    result = await evaluation_update(SchemaExecutor, CreateMutation, payload)
    evaluation_updated = assert_update(result)
    assert_same(delta, evaluation_updated)

@pytest.mark.asyncio
async def test_evaluation_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Evaluation",
        "subjectId": "3c0f46a2-f7ba-4ae5-9a07-2c21662db562"
    }
    result = await evaluation_insert(SchemaExecutor, CreateMutation, input)
    evaluation_inserted = assert_insert(result)
    payload = {
        **input,
        **evaluation_inserted
    }
    result = await evaluation_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)