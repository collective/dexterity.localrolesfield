# encoding: utf-8
from dexterity.localrolesfield.interfaces import ILocalRoleField
from dexterity.localrolesfield.interfaces import ILocalRolesField
from zope import schema
from zope.interface import implementer


@implementer(ILocalRolesField)
class LocalRolesField(schema.List):

    """Multi value local role field."""


@implementer(ILocalRoleField)
class LocalRoleField(schema.Choice):

    """Single value local role field."""
