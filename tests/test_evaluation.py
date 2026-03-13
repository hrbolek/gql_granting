import pytest
import logging
import uuid
from .asserts import assert_insert, assert_read, assert_update, assert_delete, assert_same

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

async def exam_read(SchemaExecutor, CreateQuery, variables):
    query = CreateQuery("examById")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def evaluation_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("evaluationInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def evaluation_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("evaluationUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def evaluation_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("evaluationDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_evaluation_insert(SchemaExecutor, CreateQuery, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roletype": {"name": "superadmin"}
            }]
        }
    )
    RolePermissionSchemaExtensionOverride.set_response(default_permissions)

    examId = "9575b4c5-f92a-404d-aef0-bda290a5212d"
    # exam_read_result = await exam_read(SchemaExecutor, CreateQuery, {"id": examId})
    # logging.info(f"Exam read result: {exam_read_result}")
    # exam_entity = assert_read(exam_read_result)
    # assert exam_entity["id"] == examId, f"Expected exam ID {examId}, got {exam_entity['id']}"

    input = {
        # "subjectId": "3c0f46a2-f7ba-4ae5-9a07-2c21662db562"
        "examId": examId,
        "description": "Test Evaluation",
        "parts": [
            {
                "order": 1,
                "points": 50,
                "examId": examId,
                "description": "Part 1"
            }
        ]
    }
    result = await evaluation_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_evaluation_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "order": 1,
        # "subjectId": "3c0f46a2-f7ba-4ae5-9a07-2c21662db562"
        "examId": "9575b4c5-f92a-404d-aef0-bda290a5212d"
    }
    delta = {
        "order": 2
    }
    result = await evaluation_insert(SchemaExecutor, CreateMutation, input)
    evaluation_inserted = assert_insert(result)
    payload = {
        **input,
        **evaluation_inserted,
        **delta
    }
    result = await evaluation_update(SchemaExecutor, CreateMutation, payload)
    evaluation_updated = assert_update(result)
    assert_same(delta, evaluation_updated)

@pytest.mark.asyncio
async def test_evaluation_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "examId": "9575b4c5-f92a-404d-aef0-bda290a5212d"
    }
    result = await evaluation_insert(SchemaExecutor, CreateMutation, input)
    evaluation_inserted = assert_insert(result)
    payload = {
        **input,
        **evaluation_inserted
    }
    result = await evaluation_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)