# -*- coding: utf-8 -*-

from dexterity.localrolesfield import HAS_PLONE_6
from dexterity.localrolesfield.interfaces import IDexterityLocalRolesField
from dexterity.localrolesfield.testing import LOCALROLESFIELD_FUNCTIONAL
from plone.browserlayer import utils

import unittest


if HAS_PLONE_6:
    from Products.CMFPlone.utils import get_installer


class TestSetup(unittest.TestCase):

    layer = LOCALROLESFIELD_FUNCTIONAL

    def setUp(self):
        portal = self.layer["portal"]
        if HAS_PLONE_6:
            self.installer = get_installer(portal)

    def test_product_installed(self):
        """Test if dexterity.localrolesfield is installed with portal_quickinstaller."""
        if HAS_PLONE_6:
            self.assertTrue(self.installer.is_product_installed("dexterity.localrolesfield"))

    def test_uninstall(self):
        """Test if dexterity.localrolesfield is cleanly uninstalled."""
        if HAS_PLONE_6:
            self.installer.uninstall_product("dexterity.localrolesfield")
            self.assertFalse(self.installer.is_product_installed("dexterity.localrolesfield"))

    def test_browserlayer(self):
        """Test that IDexterityLocalRolesField is registered."""
        if HAS_PLONE_6:
            self.assertIn(IDexterityLocalRolesField, utils.registered_layers())
            self.installer.uninstall_product("dexterity.localrolesfield")
            self.assertNotIn(IDexterityLocalRolesField, utils.registered_layers())
