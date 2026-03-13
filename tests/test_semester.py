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


async def semester_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("semesterInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def semester_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("semesterUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def semester_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("semesterDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_semester_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "order": 1,
        "subjectId": "3c0f46a2-f7ba-4ae5-9a07-2c21662db562"
    }
    result = await semester_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_semester_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "order": 1,
        "subjectId": "3c0f46a2-f7ba-4ae5-9a07-2c21662db562"
    }
    delta = {
        "order": 2
    }
    result = await semester_insert(SchemaExecutor, CreateMutation, input)
    semester_inserted = assert_insert(result)
    payload = {
        **input,
        **semester_inserted,
        **delta
    }
    result = await semester_update(SchemaExecutor, CreateMutation, payload)
    semester_updated = assert_update(result)
    assert_same(delta, semester_updated)

@pytest.mark.asyncio
async def test_semester_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "order": 1,
        "subjectId": "3c0f46a2-f7ba-4ae5-9a07-2c21662db562"
    }
    result = await semester_insert(SchemaExecutor, CreateMutation, input)
    semester_inserted = assert_insert(result)
    payload = {
        **input,
        **semester_inserted
    }
    result = await semester_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)