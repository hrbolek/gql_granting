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


async def lesson_type_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("lessonTypeInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def lesson_type_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("lessonTypeUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def lesson_type_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("lessonTypeDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_lesson_type_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
    result = await lesson_type_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_lesson_type_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
    result = await lesson_type_insert(SchemaExecutor, CreateMutation, input)
    lesson_type_inserted = assert_insert(result)
    payload = {
        **input,
        **lesson_type_inserted,
        **delta
    }
    result = await lesson_type_update(SchemaExecutor, CreateMutation, payload)
    lesson_type_updated = assert_update(result)
    assert_same(delta, lesson_type_updated)

@pytest.mark.asyncio
async def test_lesson_type_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Lesson",
    }
    result = await lesson_type_insert(SchemaExecutor, CreateMutation, input)
    lesson_type_inserted = assert_insert(result)
    payload = {
        **input,
        **lesson_type_inserted
    }
    result = await lesson_type_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)