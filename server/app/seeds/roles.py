from dataclasses import dataclass


@dataclass(frozen=True)
class RoleDefinition:
    name: str
    description: str
    permissions: tuple[str, ...]


ROLE_DEFINITIONS = (
    RoleDefinition(
        name="Admin",
        description="Full administrative access to the tenant.",
        permissions=(
            "members.read",
            "members.create",
            "members.update",
            "members.delete",
            "roles.read",
            "roles.create",
            "roles.update",
            "roles.delete",
            "settings.read",
            "settings.update",
            "audit_logs.read",
        ),
    ),
    RoleDefinition(
        name="Manager",
        description="Management access to tenant members and operational resources.",
        permissions=(
            "members.read",
            "members.create",
            "members.update",
            "roles.read",
            "settings.read",
            "audit_logs.read",
        ),
    ),
    RoleDefinition(
        name="Member",
        description="Standard tenant member access.",
        permissions=(
            "members.read",
            "settings.read",
        ),
    ),
    RoleDefinition(
        name="Viewer",
        description="Read-only access to permitted tenant information.",
        permissions=(
            "members.read",
            "settings.read",
            "audit_logs.read",
        ),
    ),
)
