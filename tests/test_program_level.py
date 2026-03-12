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

async def program_level_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("programLevelTypeInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def program_level_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("programLevelTypeUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def program_level_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("programLevelTypeDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_program_level_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roletype": {"name": "superadmin"}
            }]
        }
    )
    RolePermissionSchemaExtensionOverride.set_response(default_permissions)

    input = {"name": "Test Program Level"}
    result = await program_level_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_program_level_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Program Level",
    }
    delta = {
        "name": "Updated Test Program Level",
    }
    result = await program_level_insert(SchemaExecutor, CreateMutation, input)
    program_level_inserted = assert_insert(result)
    payload = {
        **input,
        **program_level_inserted,
        **delta
    }
    result = await program_level_update(SchemaExecutor, CreateMutation, payload)
    program_level_updated = assert_update(result)
    assert_same(delta, program_level_updated)

@pytest.mark.asyncio
async def test_program_level_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Program Level",
    }
    result = await program_level_insert(SchemaExecutor, CreateMutation, input)
    program_level_inserted = assert_insert(result)
    payload = {
        **input,
        **program_level_inserted
    }
    result = await program_level_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)