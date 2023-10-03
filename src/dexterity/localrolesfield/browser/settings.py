# encoding: utf-8
from collective.z3cform.datagridfield.row import DictRow
from dexterity.localroles import _ as LRMF
from dexterity.localroles.browser.settings import LocalRoleConfigurationForm
from dexterity.localroles.browser.settings import LocalRoleConfigurationPage
from dexterity.localroles.browser.settings import LocalRoleList
from dexterity.localroles.browser.settings import RelatedFormatValidator
from dexterity.localroles.browser.settings import Role
from dexterity.localroles.browser.settings import WorkflowState
from dexterity.localrolesfield import _
from dexterity.localrolesfield.utils import get_localrole_fields
from z3c.form import field
from z3c.form import validator
from zope.interface import Interface
from zope.schema import Choice
from zope.schema import Text
from zope.schema import TextLine


class ILocalRoleConfig(Interface):
    state = WorkflowState(title=LRMF(u'state'), required=True)

    value = TextLine(title=_(u'suffix'), required=False, default=u'')

    roles = Role(title=LRMF(u'roles'),
                 value_type=Choice(vocabulary='dexterity.localroles.vocabulary.SharingRolesVocabulary'),
                 required=True)

    related = Text(title=LRMF(u'related role configuration'),
                   required=False)


RelatedFieldFormatValidator = RelatedFormatValidator
validator.WidgetValidatorDiscriminators(RelatedFieldFormatValidator, field=ILocalRoleConfig['related'])


class LocalRoleFieldConfigurationForm(LocalRoleConfigurationForm):

    @property
    def fields(self):
        fields = super(LocalRoleFieldConfigurationForm, self).fields
        fields = list(fields.values())
        schema_fields = []
        for name, fti_field in get_localrole_fields(self.context.fti):
            f = LocalRoleList(
                __name__=str(name),
                title=fti_field.title,
                description=fti_field.description,
                value_type=DictRow(title=u"fieldconfig",
                                   schema=ILocalRoleConfig)
            )
            schema_fields.append(f)

        schema_fields = sorted(schema_fields, key=lambda x: x.title)
        fields.extend(schema_fields)
        return field.Fields(*fields)


class LocalRoleFieldConfigurationPage(LocalRoleConfigurationPage):
    form = LocalRoleFieldConfigurationForm
