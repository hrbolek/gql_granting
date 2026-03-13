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


async def student_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("studentInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def student_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("studentUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def student_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("studentDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_student_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "userId": "9af964f0-778c-4e07-aa4a-9fe4f36b9ac2",
        "programId": "0ac1761b-0ec7-4fc2-b4d7-127e79a316eb",
        "semesterNumber": 1
    }
    result = await student_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_student_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "userId": "9af964f0-778c-4e07-aa4a-9fe4f36b9ac2",
        "programId": "0ac1761b-0ec7-4fc2-b4d7-127e79a316eb",
        "semesterNumber": 1
    }
    delta = {
        "semesterNumber": 2
    }
    result = await student_insert(SchemaExecutor, CreateMutation, input)
    student_inserted = assert_insert(result)
    payload = {
        **input,
        **student_inserted,
        **delta
    }
    result = await student_update(SchemaExecutor, CreateMutation, payload)
    student_updated = assert_update(result)
    assert_same(delta, student_updated)

@pytest.mark.asyncio
async def test_student_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "userId": "9af964f0-778c-4e07-aa4a-9fe4f36b9ac2",
        "programId": "0ac1761b-0ec7-4fc2-b4d7-127e79a316eb",
        "semesterNumber": 1
    }
    result = await student_insert(SchemaExecutor, CreateMutation, input)
    student_inserted = assert_insert(result)
    payload = {
        **input,
        **student_inserted
    }
    result = await student_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)