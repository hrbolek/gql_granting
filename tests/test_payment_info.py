import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same

default_permissions = {
    "result": [
        {
            "roleinfo": {
                "id": "b87aed46-dfc3-40f8-ad49-03f4138c7478",
                "name": "studijní administrátor"
            }
        }
    ]
}


async def payment_info_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("paymentInfoInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def payment_info_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("paymentInfoUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def payment_info_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("paymentInfoDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_payment_info_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roleinfo": {"name": "superadmin"}
            }]
        }
    )
    RolePermissionSchemaExtensionOverride.set_response(default_permissions)

    input = {
        "SWIFT": "Test Program",
    }
    result = await payment_info_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_payment_info_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roleinfo": {"name": "superadmin"}
            }]
        }
    )
    RolePermissionSchemaExtensionOverride.set_response(default_permissions)


    input = {
        "IBAN": "Test Program",
        "SWIFT": "Test Program",
    }
    delta = {
        "IBAN": "Updated Test Program",
        "SWIFT": "Updated Test Program",
    }
    result = await payment_info_insert(SchemaExecutor, CreateMutation, input)
    payment_info_inserted = assert_insert(result)
    payload = {
        **input,
        **payment_info_inserted,
        **delta
    }
    result = await payment_info_update(SchemaExecutor, CreateMutation, payload)
    payment_info_updated = assert_update(result)
    assert_same(delta, payment_info_updated)

@pytest.mark.asyncio
async def test_payment_info_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roleinfo": {"name": "superadmin"}
            }]
        }
    )
    RolePermissionSchemaExtensionOverride.set_response(default_permissions)

    input = {
        "SWIFT": "Test Payment",
    }
    result = await payment_info_insert(SchemaExecutor, CreateMutation, input)
    payment_info_inserted = assert_insert(result)
    payload = {
        **input,
        **payment_info_inserted
    }
    result = await payment_info_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)