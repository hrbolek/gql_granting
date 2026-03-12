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


async def subject_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("subjectInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def subject_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("subjectUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def subject_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("subjectDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_subject_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Subject",
    }
    result = await subject_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_subject_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Subject",
        "nameEn": "Test Subject",
    }
    delta = {
        "name": "Updated Test Subject",
        "nameEn": "Updated Test Subject",
    }
    result = await subject_insert(SchemaExecutor, CreateMutation, input)
    subject_inserted = assert_insert(result)
    payload = {
        **input,
        **subject_inserted,
        **delta
    }
    result = await subject_update(SchemaExecutor, CreateMutation, payload)
    subject_updated = assert_update(result)
    assert_same(delta, subject_updated)

@pytest.mark.asyncio
async def test_subject_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Subject",
    }
    result = await subject_insert(SchemaExecutor, CreateMutation, input)
    subject_inserted = assert_insert(result)
    payload = {
        **input,
        **subject_inserted
    }
    result = await subject_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)