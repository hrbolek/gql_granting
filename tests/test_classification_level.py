import pytest
import logging

from .asserts import assert_read, assert_insert, assert_update, assert_delete, assert_same

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

async def classification_level_read(SchemaExecutor, CreateQuery, variables):
    query = CreateQuery("classificationLevelById")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def classification_level_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("classificationLevelInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def classification_level_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("classificationLevelUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def classification_level_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("classificationLevelDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

# @pytest.mark.asyncio
# async def test_classification_level_read(SchemaExecutor, CreateMutation, CreateQuery, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
#     WhoAmIExtensionOverride.set_user(
#         {
#             "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
#             "roles": [{
#                 "roletype": {"name": "superadmin"}
#             }]
#         }
#     )
#     RolePermissionSchemaExtensionOverride.set_response(default_permissions)

#     input = {
#         "name": "Test Program",
#     }
#     result = await classification_level_insert(SchemaExecutor, CreateMutation, input)
#     assert_insert(result)
#     result = await classification_level_read(SchemaExecutor, CreateQuery, input)

@pytest.mark.asyncio
async def test_classification_level_insert(SchemaExecutor, CreateMutation, CreateQuery, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
    }
    result = await classification_level_insert(SchemaExecutor, CreateMutation, input)
    entity = assert_insert(result)
    result = await classification_level_read(SchemaExecutor, CreateQuery, entity)
    assert_read(result)

@pytest.mark.asyncio
async def test_classification_level_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
    }
    delta = {
        "name": "Updated Test Program",
        "nameEn": "Updated Test Program",
    }
    result = await classification_level_insert(SchemaExecutor, CreateMutation, input)
    classification_level_inserted = assert_insert(result)
    payload = {
        **input,
        **classification_level_inserted,
        **delta
    }
    result = await classification_level_update(SchemaExecutor, CreateMutation, payload)
    classification_level_updated = assert_update(result)
    assert_same(delta, classification_level_updated)

@pytest.mark.asyncio
async def test_classification_level_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Classification",
    }
    result = await classification_level_insert(SchemaExecutor, CreateMutation, input)
    classification_level_inserted = assert_insert(result)
    payload = {
        **input,
        **classification_level_inserted
    }
    result = await classification_level_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)