# encoding: utf-8

from zope.component import getUtility
from plone.dexterity.interfaces import IDexterityFTI
from plone.memoize.interfaces import ICacheChooser


def fti_modified(obj, event):
    """
        When an FTI is modified, invalidate localrole fields list cache.
    """
    if not IDexterityFTI.providedBy(event.object):
        return
    cache_chooser = getUtility(ICacheChooser)
    thecache = cache_chooser('dexterity.localrolesfield.utils.get_localrole_fields')
    thecache.ramcache.invalidate('dexterity.localrolesfield.utils.get_localrole_fields')
