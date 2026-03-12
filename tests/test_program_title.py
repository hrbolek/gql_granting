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

async def program_title_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("programTitleTypeInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def program_title_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("programTitleTypeUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def program_title_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("programTitleTypeDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_program_title_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roletype": {"name": "superadmin"}
            }]
        }
    )
    RolePermissionSchemaExtensionOverride.set_response(default_permissions)

    input = {"name": "Test Program Title"}
    result = await program_title_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_program_title_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Program Title",
    }
    delta = {
        "name": "Updated Test Program Title",
    }
    result = await program_title_insert(SchemaExecutor, CreateMutation, input)
    program_title_inserted = assert_insert(result)
    payload = {
        **input,
        **program_title_inserted,
        **delta
    }
    result = await program_title_update(SchemaExecutor, CreateMutation, payload)
    program_title_updated = assert_update(result)
    assert_same(delta, program_title_updated)

@pytest.mark.asyncio
async def test_program_title_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Program Title",
    }
    result = await program_title_insert(SchemaExecutor, CreateMutation, input)
    program_title_inserted = assert_insert(result)
    payload = {
        **input,
        **program_title_inserted
    }
    result = await program_title_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)