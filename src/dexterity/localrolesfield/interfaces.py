# encoding: utf-8
from dexterity.localroles.interfaces import IDexterityLocalRoles
from zope.interface import Interface
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import IList


class IDexterityLocalRolesField(IDexterityLocalRoles):
    """Specific layer for the package"""


class IBaseLocalRoleField(Interface):

    """Base interface for local role field."""


class ILocalRolesField(IList, IBaseLocalRoleField):

    """List local roles field."""


class ILocalRoleField(IChoice, IBaseLocalRoleField):

    """Choice local roles field."""
