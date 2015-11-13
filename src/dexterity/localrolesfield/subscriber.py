# encoding: utf-8

from zope.component import getUtility
from plone.dexterity.interfaces import IDexterityFTI
from plone.memoize.interfaces import ICacheChooser

from dexterity.localroles.utility import runRelatedSearch
from dexterity.localroles.utils import add_related_roles, del_related_roles, fti_configuration

from .utils import get_localrole_fields


def fti_modified(obj, event):
    """
        When an FTI is modified, invalidate localrole fields list cache.
    """
    if not IDexterityFTI.providedBy(event.object):
        return
    cache_chooser = getUtility(ICacheChooser)
    thecache = cache_chooser('dexterity.localrolesfield.utils.get_localrole_fields')
    thecache.ramcache.invalidate('dexterity.localrolesfield.utils.get_localrole_fields')


def get_field_values(obj, name):
    values = getattr(obj, name) or []
    if not isinstance(values, (list, tuple)):
        values = [values]
    return values


def related_role_removal(obj, state, field_config, name):
    if state in field_config:
        dic = field_config[state]
        uid = obj.UID()
        for suffix in dic:
            if dic[suffix].get('rel', ''):
                related = eval(dic[suffix]['rel'])
                for utility in related:
                    if not related[utility]:
                        continue
                    for val in get_field_values(obj, name):
                        princ = suffix and '%s_%s' % (val, suffix) or val
                        for rel in runRelatedSearch(utility, obj):
                            if del_related_roles(rel, uid, princ, related[utility]):
                                rel.reindexObjectSecurity()


def related_role_addition(obj, state, field_config, name):
    if state in field_config:
        dic = field_config[state]
        uid = obj.UID()
        for suffix in dic:
            if dic[suffix].get('rel', ''):
                related = eval(dic[suffix]['rel'])
                for utility in related:
                    if not related[utility]:
                        continue
                    for val in get_field_values(obj, name):
                        princ = suffix and '%s_%s' % (val, suffix) or val
                        for rel in runRelatedSearch(utility, obj):
                            add_related_roles(rel, uid, princ, related[utility])
                            rel.reindexObjectSecurity()


def related_change_on_transition(obj, event):
    """ Set local roles on related objects after transition """
    if event.old_state.id == event.new_state.id:  # escape creation
        return
    fti_config = fti_configuration(obj)
    fti = getUtility(IDexterityFTI, name=obj.portal_type)  # Must be returned by fti_configuration
    for (name, f) in get_localrole_fields(fti):
        if name not in fti_config:
            continue
        # We have to remove the configuration linked to old state
        related_role_removal(obj, event.old_state.id, fti_config[name], name)
        # We have to add the configuration linked to new state
        related_role_addition(obj, event.new_state.id, fti_config[name], name)
