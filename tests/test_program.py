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


async def program_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("programInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def program_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("programUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def program_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("programDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_program_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "licencedGroupId": "ef1c48b7-4f65-4696-b89f-a95c2cf8814f",
        "guarantorsGroupId": "ef1c48b7-4f65-4696-b89f-a95c2cf8814f"
    }
    result = await program_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_program_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "nameEn": "Test Program",
        "licencedGroupId": "ef1c48b7-4f65-4696-b89f-a95c2cf8814f",
        "guarantorsGroupId": "ef1c48b7-4f65-4696-b89f-a95c2cf8814f"
    }
    delta = {
        "name": "Updated Test Program",
        "nameEn": "Updated Test Program",
    }
    result = await program_insert(SchemaExecutor, CreateMutation, input)
    program_inserted = assert_insert(result)
    payload = {
        **input,
        **program_inserted,
        **delta
    }
    result = await program_update(SchemaExecutor, CreateMutation, payload)
    program_updated = assert_update(result)
    assert_same(delta, program_updated)

@pytest.mark.asyncio
async def test_program_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "licencedGroupId": "ef1c48b7-4f65-4696-b89f-a95c2cf8814f",
        "guarantorsGroupId": "ef1c48b7-4f65-4696-b89f-a95c2cf8814f"
    }
    result = await program_insert(SchemaExecutor, CreateMutation, input)
    program_inserted = assert_insert(result)
    payload = {
        **input,
        **program_inserted
    }
    result = await program_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)