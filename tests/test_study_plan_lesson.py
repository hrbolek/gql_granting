import pytest
import logging

import functools
import re

def snake_to_camel(name):
    parts = name.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])

def fromSchema(*, camel_case_name=None, query_name=None):
    def decorator(func):
        mutation_name = snake_to_camel(func.__name__) if camel_case_name else func.__name__
        if query_name:
            mutation_name = query_name

        @functools.wraps(func)
        async def wrapper(SchemaExecutor, CreateMutation, variables):
            query = CreateMutation(mutation_name)
            return await SchemaExecutor(query, variables)

        return wrapper
    return decorator

from .asserts import assert_insert, assert_typename_with_error, assert_update, assert_delete, assert_same

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

async def study_plan_lesson_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("studyPlanLessonInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def study_plan_lesson_add_instructor(SchemaExecutor, CreateMutation, variables):
    logging.info(f"study_plan_lesson_add_instructor.variables: {variables}")
    query = CreateMutation("studyPlanLessonAddInstructor")
    logging.info(f"study_plan_lesson_add_instructor.query: {query}")
    result = await SchemaExecutor(query=query, variable_values=variables)
    logging.info(f"study_plan_lesson_add_instructor.result: {result}")
    return result

async def study_plan_lesson_remove_instructor(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("studyPlanLessonRemoveInstructor")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def study_plan_lesson_add_facility(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("studyPlanLessonAddFacility")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def study_plan_lesson_remove_facility(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("studyPlanLessonRemoveFacility")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def study_plan_lesson_add_group(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("studyPlanLessonAddGroup")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def study_plan_lesson_remove_group(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("studyPlanLessonRemoveGroup")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def study_plan_lesson_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("studyPlanLessonUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def study_plan_lesson_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("studyPlanLessonDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_study_plan_lesson_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Program Form",
        "nameEn": "Test Program Form",
        "planId": "8bde6144-7b82-46d1-ba38-aaab9fa54191",
        "lessontypeId": "e2b7cbf6-95e1-11ed-a1eb-0242ac120002",
        "topicId": "ef1c48b7-4f65-4696-b89f-a95c2cf8814f"
    }
    result = await study_plan_lesson_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_study_plan_lesson_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Program Form",
        "nameEn": "Test Program Form",
        "planId": "8bde6144-7b82-46d1-ba38-aaab9fa54191",
        "lessontypeId": "e2b7cbf6-95e1-11ed-a1eb-0242ac120002",
        "topicId": "ef1c48b7-4f65-4696-b89f-a95c2cf8814f"
    }
    delta = {
        "name": "Updated Test Program Form",
    }
    result = await study_plan_lesson_insert(SchemaExecutor, CreateMutation, input)
    study_plan_lesson_inserted = assert_insert(result)
    payload = {
        **input,
        **study_plan_lesson_inserted,
        **delta
    }
    result = await study_plan_lesson_update(SchemaExecutor, CreateMutation, payload)
    study_plan_lesson_updated = assert_update(result)
    assert_same(delta, study_plan_lesson_updated)

@pytest.mark.asyncio
async def test_study_plan_lesson_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "name": "Test Program Form",
        "nameEn": "Test Program Form",
        "planId": "8bde6144-7b82-46d1-ba38-aaab9fa54191",
        "lessontypeId": "e2b7cbf6-95e1-11ed-a1eb-0242ac120002",
        "topicId": "ef1c48b7-4f65-4696-b89f-a95c2cf8814f"
    }
    result = await study_plan_lesson_insert(SchemaExecutor, CreateMutation, input)
    study_plan_lesson_inserted = assert_insert(result)
    payload = {
        **input,
        **study_plan_lesson_inserted
    }
    result = await study_plan_lesson_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)


@pytest.mark.asyncio
async def test_study_plan_lesson_add_remove_instructor(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roletype": {"name": "superadmin"}
            }]
        }
    )
    RolePermissionSchemaExtensionOverride.set_response(default_permissions)

    planitemId = "a46453ff-1246-4797-8323-6f44d04a3e50"
    input = {
        "id": planitemId,
        "name": "Test Program Form",
        "nameEn": "Test Program Form",
        "planId": "8bde6144-7b82-46d1-ba38-aaab9fa54191",
        "lessontypeId": "e2b7cbf6-95e1-11ed-a1eb-0242ac120002",
        "topicId": "ef1c48b7-4f65-4696-b89f-a95c2cf8814f"
    }

    delta = {
        "name": "Updated Test Program Form",
    }
    # logging.info("Inserting study plan lesson")
    result = await study_plan_lesson_insert(SchemaExecutor, CreateMutation, input)
    study_plan_lesson_inserted = assert_insert(result)

    input = {
        "planitemId": planitemId,
        "userId": "fac5118e-ab8b-42c0-bad0-7095db4d0d19",
    }

    payload = {
        **input,
        **study_plan_lesson_inserted,
        **delta
    }
    
    result = await study_plan_lesson_remove_instructor(SchemaExecutor, CreateMutation, payload)
    assert_typename_with_error(result, code="a8b820e1-2659-4605-94ba-4373900dd98f")

    result = await study_plan_lesson_add_instructor(SchemaExecutor, CreateMutation, payload)
    study_plan_lesson_inserted = assert_update(result)
    payload = {
        **input,
        **study_plan_lesson_inserted,
        **delta
    }
    # logging.info("Removing instructor from study plan lesson")
    result = await study_plan_lesson_add_instructor(SchemaExecutor, CreateMutation, payload)
    assert_typename_with_error(result, code="1f7fe358-c83b-4ecb-8aeb-a042b139356e")

    result = await study_plan_lesson_remove_instructor(SchemaExecutor, CreateMutation, payload)
    study_plan_lesson_updated = assert_update(result)

@pytest.mark.asyncio
async def test_study_plan_lesson_add_remove_instructor_failed(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roletype": {"name": "superadmin"}
            }]
        }
    )
    RolePermissionSchemaExtensionOverride.set_response(default_permissions)

    planitemId = "645a6375-fb13-41a1-9d36-352c9d1199fa"

    input = {
        "planitemId": planitemId,
        "userId": "fac5118e-ab8b-42c0-bad0-7095db4d0d19",
    }

    result = await study_plan_lesson_add_instructor(SchemaExecutor, CreateMutation, input)
    assert_typename_with_error(result)
    
    result = await study_plan_lesson_remove_instructor(SchemaExecutor, CreateMutation, input)
    assert_typename_with_error(result)



@pytest.mark.asyncio
async def test_study_plan_lesson_add_remove_facility(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roletype": {"name": "superadmin"}
            }]
        }
    )
    RolePermissionSchemaExtensionOverride.set_response(default_permissions)

    planitemId = "63e4ead1-e03b-48a8-89e9-d9de6d93d02d"
    input = {
        "id": planitemId,
        "name": "Test Program Form",
        "nameEn": "Test Program Form",
        "planId": "8bde6144-7b82-46d1-ba38-aaab9fa54191",
        "lessontypeId": "e2b7cbf6-95e1-11ed-a1eb-0242ac120002",
        "topicId": "ef1c48b7-4f65-4696-b89f-a95c2cf8814f"
    }

    delta = {
        "name": "Updated Test Program Form",
    }
    result = await study_plan_lesson_insert(SchemaExecutor, CreateMutation, input)
    study_plan_lesson_inserted = assert_insert(result)

    input = {
        "planitemId": planitemId,
        "facilityId": "e51cab3a-7799-44b9-92df-6e899e28f155",
    }

    payload = {
        **input,
        **study_plan_lesson_inserted,
        **delta
    }
    result = await study_plan_lesson_remove_facility(SchemaExecutor, CreateMutation, payload)
    assert_typename_with_error(result, code="b69dde53-4c7f-4909-8025-1874165db8d8")

    result = await study_plan_lesson_add_facility(SchemaExecutor, CreateMutation, payload)
    study_plan_lesson_inserted = assert_update(result)

    result = await study_plan_lesson_add_facility(SchemaExecutor, CreateMutation, payload)
    assert_typename_with_error(result, code="36983127-5d52-4bd5-b4ee-5c01665589ba")

    payload = {
        **input,
        **study_plan_lesson_inserted,
        **delta
    }
    result = await study_plan_lesson_remove_facility(SchemaExecutor, CreateMutation, payload)
    study_plan_lesson_updated = assert_update(result)



@pytest.mark.asyncio
async def test_study_plan_lesson_add_remove_facility_failed(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roletype": {"name": "superadmin"}
            }]
        }
    )
    RolePermissionSchemaExtensionOverride.set_response(default_permissions)

    planitemId = "645a6375-fb13-41a1-9d36-352c9d1199fa"
    payload = {
        "planitemId": planitemId,
        "facilityId": "e51cab3a-7799-44b9-92df-6e899e28f155",
    }

    result = await study_plan_lesson_add_facility(SchemaExecutor, CreateMutation, payload)
    assert_typename_with_error(result)

    result = await study_plan_lesson_remove_facility(SchemaExecutor, CreateMutation, payload)
    assert_typename_with_error(result)



@pytest.mark.asyncio
async def test_study_plan_lesson_add_remove_study_group(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roletype": {"name": "superadmin"}
            }]
        }
    )
    RolePermissionSchemaExtensionOverride.set_response(default_permissions)

    planitemId = "8aedcff6-28d1-41c1-a2b2-3918083335ce"
    input = {
        "id": planitemId,
        "name": "Test Program Form",
        "nameEn": "Test Program Form",
        "planId": "8bde6144-7b82-46d1-ba38-aaab9fa54191",
        "lessontypeId": "e2b7cbf6-95e1-11ed-a1eb-0242ac120002",
        "topicId": "ef1c48b7-4f65-4696-b89f-a95c2cf8814f"
    }

    delta = {
        "name": "Updated Test Program Form",
    }
    result = await study_plan_lesson_insert(SchemaExecutor, CreateMutation, input)
    study_plan_lesson_inserted = assert_insert(result)

    input = {
        "planitemId": planitemId,
        "groupId": "5f566690-a5a6-4e3c-8a20-1eabc8654499",
    }

    payload = {
        **input,
        **study_plan_lesson_inserted,
        **delta
    }
    result = await study_plan_lesson_remove_group(SchemaExecutor, CreateMutation, payload)
    assert_typename_with_error(result, code="4d7798dc-24e4-4d37-886b-7f1dda701fd0")

    result = await study_plan_lesson_add_group(SchemaExecutor, CreateMutation, payload)
    study_plan_lesson_inserted = assert_update(result)
    payload = {
        **input,
        **study_plan_lesson_inserted,
        **delta
    }
    result = await study_plan_lesson_add_group(SchemaExecutor, CreateMutation, payload)
    assert_typename_with_error(result, code="f866f8ed-a47e-4c6a-8e29-e68e22ebb1a5")

    result = await study_plan_lesson_remove_group(SchemaExecutor, CreateMutation, payload)
    study_plan_lesson_updated = assert_update(result)


@pytest.mark.asyncio
async def test_study_plan_lesson_add_remove_study_group_failed(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
    WhoAmIExtensionOverride.set_user(
        {
            "id": "30bc16ac-946a-4d73-a1ad-3fd3ddd038f7",
            "roles": [{
                "roletype": {"name": "superadmin"}
            }]
        }
    )
    RolePermissionSchemaExtensionOverride.set_response(default_permissions)

    planitemId = "645a6375-fb13-41a1-9d36-352c9d1199fa"
    input = {
        "planitemId": planitemId,
        "groupId": "5f566690-a5a6-4e3c-8a20-1eabc8654499",
    }

    result = await study_plan_lesson_add_group(SchemaExecutor, CreateMutation, input)
    assert_typename_with_error(result)

    result = await study_plan_lesson_remove_group(SchemaExecutor, CreateMutation, input)
    assert_typename_with_error(result)


