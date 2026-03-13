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


async def admission_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("admissionInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def admission_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("admissionUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def admission_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("admissionDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_admission_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "programId": "0ac1761b-0ec7-4fc2-b4d7-127e79a316eb",
    }
    result = await admission_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_admission_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "programId": "0ac1761b-0ec7-4fc2-b4d7-127e79a316eb",
        "name": "Admissions 2026/27"
    }
    delta = {
        "name": "Admissions 2027/28"
    }
    result = await admission_insert(SchemaExecutor, CreateMutation, input)
    admission_inserted = assert_insert(result)
    payload = {
        **input,
        **admission_inserted,
        **delta
    }
    result = await admission_update(SchemaExecutor, CreateMutation, payload)
    admission_updated = assert_update(result)
    assert_same(delta, admission_updated)

@pytest.mark.asyncio
async def test_admission_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "programId": "0ac1761b-0ec7-4fc2-b4d7-127e79a316eb",
        "name": "Admissions 2026/27"
    }
    result = await admission_insert(SchemaExecutor, CreateMutation, input)
    admission_inserted = assert_insert(result)
    payload = {
        **input,
        **admission_inserted
    }
    result = await admission_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)