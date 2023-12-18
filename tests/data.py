

readonly = {'read'}
crud = {'create', 'read', 'update', 'delete'}
edit = {'read', 'update'}
create = {'create', 'read', 'update'}
attach = {'attach', 'detach'}

SUPER_EMAIL = 'super@gmail.com'
VERIFIED_EMAIL = 'verified@gmail.com'
CUSTOM_GROUP_EMAIL = 'customgroup@gmail.com'
CUSTOM_PERMISSIONS_EMAIL = 'custompermissions@gmail.com'
BANNED_EMAIL = 'banned@gmail.com'
INACTIVE_EMAIL = 'inactive@gmail.com'
UNVERIFIED_EMAIL = 'unverified@gmail.com'
DELETED_EMAIL = 'deleted@gmail.com'
ADMIN_EMAIL = 'admin@gmail.com'

# DO NOT CHANGE ANYTHING HERE OR SOME TESTS WOULD FAIL
# Only list down unique permissions
GROUP_FIXTURES_DEV: dict[str, dict] = {
    'admin': {
        'description': 'Administrative actions',
        # 'role': {*create, *attach, 'reset'},
        'group': {*create, *attach, 'reset'},
        # 'permission': [*crud, *attach],
    },
    'account': {
        'description': 'Account management',
        # 'account': crud,
        # 'ban': attach,
        # 'role': edit,
        'group': attach,
        # 'permission': attach,
    },
    'base': {
        'description': 'Required account permissions',
        # 'profile': edit,
        # 'settings': edit,
        # 'post': crud,
        # 'dashboard': readonly,
    },
    'empty': {
        'description': 'Nothing here',
    },
}
# GROUP_FIXTURES_PROD = {**GROUP_FIXTURES_DEV}

groups = {'base', 'message'}
ROLE_FIXTURES = {
    'super': {*groups, 'account', 'admin', 'message'},
    'admin': {*groups, 'account', 'admin', 'message'},
    'moderator': {*groups, 'account'},
    'user': groups,
}