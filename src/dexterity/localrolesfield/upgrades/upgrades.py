# -*- coding: utf-8 -*-
from ..utils import get_localrole_fields
from persistent.mapping import PersistentMapping
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFPlone.utils import base_hasattr
from zope.component import getUtilitiesFor

import logging


logger = logging.getLogger('dexterity.localroles: upgrade. ')


def v2(context):
    for (name, fti) in getUtilitiesFor(IDexterityFTI):
        for (fname, field) in get_localrole_fields(fti):
            if not base_hasattr(fti, fname):
                continue
            logger.info("FTI '%s' => Copying old field config '%s': '%s'" % (name, fname, getattr(fti, fname)))
            if not base_hasattr(fti, 'localroles'):
                setattr(fti, 'localroles', PersistentMapping())
            fti.localroles[fname] = {}
            for state_key, state_dic in getattr(fti, fname).items():
                fti.localroles[fname][state_key] = {}
                for principal, roles in state_dic.items():
                    fti.localroles[fname][state_key][principal] = {'roles': roles}
            delattr(fti, fname)
