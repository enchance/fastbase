from fastbase.schemas import GroupEnum


crud = {'create', 'read', 'update', 'delete'}
read = {'read'}
edit = {'read', 'update'}

SUPER_EMAIL = 'super@gmail.com'
FIXTURE_PASSWORD = 'pass123'        #


# DO NOT CHANGE ANYTHING HERE OR SOME TESTS WOULD FAIL
# Only list down unique permissions
GROUP_FIXTURES_DEV: dict[str, dict] = {
    GroupEnum.AdminGroup: {
        'description': 'Administrative actions',
        'foo': crud,
    },
    GroupEnum.AccountGroup: {
        'description': 'Basic account management',
        'bar': read,
    },
    'UploadGroup': {
        'description': 'Upload files for specific areas',
        'baz': edit
    },
    'EmptyGroup': {
        'description': 'Nothing here',
    },
}

groups = {'AccountGroup', 'UploadGroup'}
ROLE_FIXTURES = {
    'super': {*groups, GroupEnum.AdminGroup},
    'admin': {*groups, GroupEnum.AdminGroup},
    'user': groups,
}