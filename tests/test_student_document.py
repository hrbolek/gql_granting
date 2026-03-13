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

async def student_document_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("studentDocumentInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def student_document_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("studentDocumentUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def student_document_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("studentDocumentDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_student_document_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "studentId": "bc7e2bb3-c215-4cf7-bc39-d271f1bf0627",
        "documentId": "f45925a0-d56b-43d0-a516-5005db4f9068",
    }
    result = await student_document_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_student_document_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "studentId": "bc7e2bb3-c215-4cf7-bc39-d271f1bf0627",
        "documentId": "f45925a0-d56b-43d0-a516-5005db4f9068",
    }
    delta = {
        # "eventId": "944bb9e1-4e14-4f70-8050-c804474e1526"
    }
    result = await student_document_insert(SchemaExecutor, CreateMutation, input)
    student_document_inserted = assert_insert(result)
    payload = {
        **input,
        **student_document_inserted,
        **delta
    }
    result = await student_document_update(SchemaExecutor, CreateMutation, payload)
    student_document_updated = assert_update(result)
    assert_same(delta, student_document_updated)

@pytest.mark.asyncio
async def test_student_document_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "studentId": "bc7e2bb3-c215-4cf7-bc39-d271f1bf0627",
        "documentId": "f45925a0-d56b-43d0-a516-5005db4f9068",
    }
    result = await student_document_insert(SchemaExecutor, CreateMutation, input)
    student_document_inserted = assert_insert(result)
    payload = {
        **input,
        **student_document_inserted
    }
    result = await student_document_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)