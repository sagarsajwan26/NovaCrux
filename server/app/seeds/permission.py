from dataclasses import dataclass


@dataclass(frozen=True)
class PermissionDefinition:
    resource: str
    action: str
    description: str


PERMISSIONS = [
    PermissionDefinition(
        resource="members", action="read", description="View tenant members."
    ),
    PermissionDefinition(
        resource="members", action="create", description="add members to a tenant"
    ),
    PermissionDefinition(
        resource="members",
        action="update",
        description="Update tenant members.",
    ),
    PermissionDefinition(
        resource="members",
        action="delete",
        description="Remove members from a tenant.",
    ),
    PermissionDefinition(
        resource="roles",
        action="read",
        description="View tenant roles.",
    ),
    PermissionDefinition(
        resource="roles",
        action="create",
        description="Create tenant roles.",
    ),
    PermissionDefinition(
        resource="roles",
        action="update",
        description="Update tenant roles.",
    ),
    PermissionDefinition(
        resource="roles",
        action="delete",
        description="Delete tenant roles.",
    ),
    PermissionDefinition(
        resource="settings",
        action="read",
        description="View tenant settings.",
    ),
    PermissionDefinition(
        resource="settings",
        action="update",
        description="Update tenant settings.",
    ),
    PermissionDefinition(
        resource="audit_logs",
        action="read",
        description="View tenant audit logs.",
    ),
]
