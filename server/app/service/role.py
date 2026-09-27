from sqlalchemy.ext.asyncio import AsyncSession
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.role_permission_repository import RolePermissionRepository
from app.seeds.roles import ROLE_DEFINITIONS


class RoleService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.role_repository = RoleRepository(db)
        self.permission_repository = PermissionRepository(db)
        self.role_permission_repository = RolePermissionRepository(db)

    async def create_default_roles(
        self,
        tenant_id: int,
    ) -> list[Role]:
        created_roles: list[Role] = []

        for definition in ROLE_DEFINITIONS:
            existing_role = await self.role_repository.get_by_name(
                tenant_id=tenant_id, name=definition.name
            )
            if existing_role:
                created_roles.append(existing_role)
                continue

            role = Role(
                tenant_id=tenant_id,
                name=definition.name,
                description=definition.description,
                is_system=True,
            )
            role = await self.role_repository.create(role)

            for permission_name in definition.permissions:
                resource, action = permission_name.split(".", 1)
                permission = (
                    await self.permission_repository.get_by_resource_and_action(
                        resource=resource, action=action
                    )
                )

                if permission is None:
                    raise ValueError(f"Permission '{permission_name}' does not exists")

                already_assigned = await self.role_permission_repository.exists(
                    role_id=role.id, permission_id=permission.id
                )

                if already_assigned:
                    continue

                role_permission = RolePermission(
                    role_id=role.id, permission_id=permission.id
                )

                await self.role_permission_repository.create(role_permission)
            created_roles.append(role)

        return created_roles
