import pytest
import logging

from .asserts import assert_insert, assert_update, assert_delete, assert_same, assert_typename_with_error

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


async def exam_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("examInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def exam_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("examUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def exam_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("examDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_exam_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Exam",
        "planId": "8bde6144-7b82-46d1-ba38-aaab9fa54191",
        "typeId": "a00a0322-b095-11ed-9bd8-0242ac110002"
    }
    result = await exam_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)
    logging.info(f"Exam insert result: {result}")

@pytest.mark.asyncio
async def test_exam_insert_failed(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Exam",
        "planId": "7e6fd5cd-43e1-4cff-8b96-a8a218f526d3",
        "typeId": "7e6fd5cd-43e1-4cff-8b96-a8a218f526d3"
    }
    result = await exam_insert(SchemaExecutor, CreateMutation, input)
    assert_typename_with_error(result)



@pytest.mark.asyncio
async def test_exam_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Exam",
        "nameEn": "Test Exam",
        "planId": "8bde6144-7b82-46d1-ba38-aaab9fa54191",
        "typeId": "a00a0322-b095-11ed-9bd8-0242ac110002"
    }
    delta = {
        "name": "Updated Test Exam",
        "nameEn": "Updated Test Exam",
    }
    result = await exam_insert(SchemaExecutor, CreateMutation, input)
    exam_inserted = assert_insert(result)
    payload = {
        **input,
        **exam_inserted,
        **delta
    }
    result = await exam_update(SchemaExecutor, CreateMutation, payload)
    exam_updated = assert_update(result)
    assert_same(delta, exam_updated)

@pytest.mark.asyncio
async def test_exam_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Exam",
        "planId": "8bde6144-7b82-46d1-ba38-aaab9fa54191",
        "typeId": "a00a0322-b095-11ed-9bd8-0242ac110002"
    }
    result = await exam_insert(SchemaExecutor, CreateMutation, input)
    exam_inserted = assert_insert(result)
    payload = {
        **input,
        **exam_inserted
    }
    result = await exam_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)