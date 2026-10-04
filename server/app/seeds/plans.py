from app.models.plans import BillingInterval, PlanCode
from dataclasses import dataclass


@dataclass(frozen=True)
class EntitlementDefinition:
    feature_key: str
    enabled: bool = False
    limit_value: int | None = None
    config: dict | None = None


@dataclass(frozen=True)
class PlanDefinition:
    code: PlanCode
    name: str
    description: str
    billing_interval: BillingInterval | None
    price: int
    entitlements: tuple[EntitlementDefinition, ...]


PLAN_DEFINITIONS = (
    PlanDefinition(
        code=PlanCode.FREE,
        name="Free",
        description="Free NovaCrux website and platform access.",
        billing_interval=None,
        price=0,
        entitlements=(
            EntitlementDefinition(
                "website.custom_branding",
                enabled=False,
            ),
            EntitlementDefinition(
                "website.custom_favicon",
                enabled=False,
            ),
            EntitlementDefinition(
                "website.custom_fonts",
                enabled=False,
            ),
            EntitlementDefinition(
                "website.custom_domain",
                enabled=False,
            ),
            EntitlementDefinition(
                "website.remove_branding",
                enabled=False,
            ),
            EntitlementDefinition(
                "website.max_pages",
                enabled=True,
                limit_value=3,
            ),
            EntitlementDefinition(
                "website.max_sections",
                enabled=True,
                limit_value=10,
            ),
            EntitlementDefinition(
                "website.publish_frequency",
                enabled=True,
                config={
                    "period": "day",
                    "max_updates": 1,
                },
            ),
        ),
    ),
    PlanDefinition(
        code=PlanCode.BASIC,
        name="Basic",
        description="Basic website customization and tenant capabilities.",
        billing_interval=BillingInterval.MONTHLY,
        price=0,
        entitlements=(
            EntitlementDefinition(
                "website.custom_branding",
                enabled=True,
            ),
            EntitlementDefinition(
                "website.custom_favicon",
                enabled=True,
            ),
            EntitlementDefinition(
                "website.custom_fonts",
                enabled=False,
            ),
            EntitlementDefinition(
                "website.custom_domain",
                enabled=False,
            ),
            EntitlementDefinition(
                "website.remove_branding",
                enabled=False,
            ),
            EntitlementDefinition(
                "website.max_pages",
                enabled=True,
                limit_value=10,
            ),
            EntitlementDefinition(
                "website.max_sections",
                enabled=True,
                limit_value=30,
            ),
            EntitlementDefinition(
                "website.publish_frequency",
                enabled=True,
                config={
                    "period": "day",
                    "max_updates": 5,
                },
            ),
        ),
    ),
    PlanDefinition(
        code=PlanCode.STANDARD,
        name="Standard",
        description="Advanced website customization and tenant capabilities.",
        billing_interval=BillingInterval.MONTHLY,
        price=0,
        entitlements=(
            EntitlementDefinition(
                "website.custom_branding",
                enabled=True,
            ),
            EntitlementDefinition(
                "website.custom_favicon",
                enabled=True,
            ),
            EntitlementDefinition(
                "website.custom_fonts",
                enabled=True,
            ),
            EntitlementDefinition(
                "website.custom_domain",
                enabled=True,
            ),
            EntitlementDefinition(
                "website.remove_branding",
                enabled=True,
            ),
            EntitlementDefinition(
                "website.max_pages",
                enabled=True,
                limit_value=50,
            ),
            EntitlementDefinition(
                "website.max_sections",
                enabled=True,
                limit_value=100,
            ),
            EntitlementDefinition(
                "website.publish_frequency",
                enabled=True,
                config={
                    "period": "day",
                    "max_updates": 20,
                },
            ),
        ),
    ),
    PlanDefinition(
        code=PlanCode.PREMIUM,
        name="Premium",
        description="Full NovaCrux website customization and capabilities.",
        billing_interval=BillingInterval.YEARLY,
        price=0,
        entitlements=(
            EntitlementDefinition(
                "website.custom_branding",
                enabled=True,
            ),
            EntitlementDefinition(
                "website.custom_favicon",
                enabled=True,
            ),
            EntitlementDefinition(
                "website.custom_fonts",
                enabled=True,
            ),
            EntitlementDefinition(
                "website.custom_domain",
                enabled=True,
            ),
            EntitlementDefinition(
                "website.remove_branding",
                enabled=True,
            ),
            EntitlementDefinition(
                "website.max_pages",
                enabled=True,
                limit_value=250,
            ),
            EntitlementDefinition(
                "website.max_sections",
                enabled=True,
                limit_value=500,
            ),
            EntitlementDefinition(
                "website.publish_frequency",
                enabled=True,
                config={
                    "period": "day",
                    "max_updates": 100,
                },
            ),
        ),
    ),
)
