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


async def payment_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("paymentInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def payment_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("paymentUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def payment_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("paymentDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_payment_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roletype": {"name": "superadmin"}
            }]
        }
    )
    RolePermissionSchemaExtensionOverride.set_response(default_permissions)

    from .test_payment_info import payment_info_insert
    paymentId = "5eead68b-4a51-4145-a5ee-0d4ca6e2e681"
    payment_result = await payment_info_insert(SchemaExecutor, CreateMutation, variables={
        "id": paymentId
    })
    assert_insert(payment_result)

    input = {
        "programId": "0ac1761b-0ec7-4fc2-b4d7-127e79a316eb",
        "studentId": "bc7e2bb3-c215-4cf7-bc39-d271f1bf0627",
        "paymentInfoId": paymentId
    }
    result = await payment_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_payment_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roletype": {"name": "superadmin"}
            }]
        }
    )
    RolePermissionSchemaExtensionOverride.set_response(default_permissions)


    from .test_payment_info import payment_info_insert
    paymentId = "011f3f26-f986-4f61-9439-dc5c5793f595"
    payment_result = await payment_info_insert(SchemaExecutor, CreateMutation, variables={
        "id": paymentId
    })
    assert_insert(payment_result)

    input = {
        "programId": "0ac1761b-0ec7-4fc2-b4d7-127e79a316eb",
        "studentId": "bc7e2bb3-c215-4cf7-bc39-d271f1bf0627",
        "paymentInfoId": paymentId,
        "variableSymbol": "IBAN"
    }
    delta = {
        "variableSymbol": "IBAN256"
    }

    result = await payment_insert(SchemaExecutor, CreateMutation, input)
    payment_inserted = assert_insert(result)
    payload = {
        **input,
        **payment_inserted,
        **delta
    }
    result = await payment_update(SchemaExecutor, CreateMutation, payload)
    payment_updated = assert_update(result)
    assert_same(delta, payment_updated)

@pytest.mark.asyncio
async def test_payment_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roletype": {"name": "superadmin"}
            }]
        }
    )
    RolePermissionSchemaExtensionOverride.set_response(default_permissions)

    from .test_payment_info import payment_info_insert
    paymentId = "323f5136-3c0e-4ebc-81bc-f8c6f37d0f18"
    payment_result = await payment_info_insert(SchemaExecutor, CreateMutation, variables={
        "id": paymentId
    })
    assert_insert(payment_result)

    input = {
        "programId": "0ac1761b-0ec7-4fc2-b4d7-127e79a316eb",
        "studentId": "bc7e2bb3-c215-4cf7-bc39-d271f1bf0627",
        "paymentInfoId": paymentId
    }
    result = await payment_insert(SchemaExecutor, CreateMutation, input)
    payment_inserted = assert_insert(result)
    payload = {
        **input,
        **payment_inserted
    }
    payment_inserted = await payment_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(payment_inserted)