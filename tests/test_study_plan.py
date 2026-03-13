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

async def study_plan_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("studyPlanInsert")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def study_plan_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("studyPlanUpdate")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result

async def study_plan_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("studyPlanDelete")
    result = await SchemaExecutor(query=query, variable_values=variables)
    return result


@pytest.mark.asyncio
async def test_study_plan_insert(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "semesterId": "49ac365e-c9be-4752-9a46-21542ed361df",
        "eventId": "2144343a-da78-41f8-89e5-36b3214f635a"
    }
    result = await study_plan_insert(SchemaExecutor, CreateMutation, input)
    assert_insert(result)

@pytest.mark.asyncio
async def test_study_plan_update(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "semesterId": "49ac365e-c9be-4752-9a46-21542ed361df",
        "eventId": "2144343a-da78-41f8-89e5-36b3214f635a"
    }
    delta = {
        "eventId": "944bb9e1-4e14-4f70-8050-c804474e1526"
    }
    result = await study_plan_insert(SchemaExecutor, CreateMutation, input)
    study_plan_inserted = assert_insert(result)
    payload = {
        **input,
        **study_plan_inserted,
        **delta
    }
    result = await study_plan_update(SchemaExecutor, CreateMutation, payload)
    study_plan_updated = assert_update(result)
    assert_same(delta, study_plan_updated)

@pytest.mark.asyncio
async def test_study_plan_delete(SchemaExecutor, CreateMutation, WhoAmIExtensionOverride, RolePermissionSchemaExtensionOverride):
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
        "semesterId": "49ac365e-c9be-4752-9a46-21542ed361df",
        "eventId": "2144343a-da78-41f8-89e5-36b3214f635a"
    }
    result = await study_plan_insert(SchemaExecutor, CreateMutation, input)
    study_plan_inserted = assert_insert(result)
    payload = {
        **input,
        **study_plan_inserted
    }
    result = await study_plan_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)