# -*- coding: utf-8 -*-
import unittest2 as unittest
from plone import api
from plone.app.testing import login, TEST_USER_NAME, setRoles, TEST_USER_ID

from dexterity.localroles.utils import add_fti_configuration, get_related_roles

from ..testing import LOCALROLESFIELD_FUNCTIONAL


class TestSubscriber(unittest.TestCase):

    layer = LOCALROLESFIELD_FUNCTIONAL

    def setUp(self):
        super(TestSubscriber, self).setUp()
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        field_config = {
            u'private': {
                'editor': {'roles': ('Editor', 'Reader'), 'rel': "{'dexterity.localroles.related_parent':['Editor']}"},
                'reviewer': {'roles': ('Contributor', 'Reader')},
            },
            u'published': {
                'editor': {'roles': ('Reader', ), 'rel': "{'dexterity.localroles.related_parent':['Reader']}"},
                'reviewer': {'roles': ('Editor', 'Contributor', 'Reader')},
            },
        }
        userfield_config = {
            u'private': {
                None: {'roles': ('Reader', ), 'rel': "{'dexterity.localroles.related_parent':['Reader']}"},
            },
            u'published': {
                None: {'roles': ('Editor', ), 'rel': "{'dexterity.localroles.related_parent':['Editor']}"},
            },
        }
        global_config = {
            u'private': {
                'kate': {'roles': ('Editor', )},
            },
        }
        behavior_field_config = {
            u'private': {
                None: {'roles': ('Reviewer', ), 'rel': "{'dexterity.localroles.related_parent':['Reviewer']}"},
            },
        }
        add_fti_configuration('testingtype', global_config, keyname='static_config')
        add_fti_configuration('testingtype', field_config, keyname='localrole_field')
        add_fti_configuration('testingtype', userfield_config, keyname='localrole_user_field')
        add_fti_configuration('testingtype', behavior_field_config, keyname='mono_localrole_field')

        self.item = api.content.create(container=self.portal, type='testingtype',
                                       id='testlocalroles', title='TestLocalRoles',
                                       localrole_field=[u'mail'],
                                       localrole_user_field=[u'john', u'kate'],
                                       mono_localrole_field=u'john')

    def test_related_change_on_transition(self):
        api.content.transition(obj=self.item, transition='publish')
        self.assertDictEqual(get_related_roles(self.portal, self.item.UID()),
                             {u'mail_editor': set(['Reader']), u'john': set(['Editor']),
                              u'kate': set(['Editor'])})

    def test_related_change_on_addition(self):
        self.assertDictEqual(get_related_roles(self.portal, self.item.UID()),
                             {u'mail_editor': set(['Editor']), u'john': set(['Reviewer', 'Reader']),
                              u'kate': set(['Reader'])})

    def test_related_change_on_removal(self):
        # The parent is set by addition subscriber
        self.assertDictEqual(get_related_roles(self.portal, self.item.UID()),
                             {u'mail_editor': set(['Editor']), u'john': set(['Reviewer', 'Reader']),
                              u'kate': set(['Reader'])})
        api.content.delete(obj=self.item)
        # The parent is changed
        self.assertDictEqual(get_related_roles(self.portal, self.item.UID()), {})
