import pytest
from GraphTypeDefinitions import schema
import datetime
# from ..shared import (
#     prepare_demodata,
#     prepare_in_memory_sqllite,
#     get_demodata,
#     createContext,
# )
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)
test_reference_lesson_types = createResolveReferenceTest(tableName='aclessontypes', gqltype='AcLessonTypeGQLModel', attributeNames=["id"])
