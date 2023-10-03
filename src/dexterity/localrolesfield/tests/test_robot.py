# encoding: utf-8

from dexterity.localrolesfield import testing
from plone.testing import layered
from robotsuite import RobotTestSuite


def test_suite():
    return layered(RobotTestSuite('robot'),
                   layer=testing.LOCALROLESFIELD_ROBOT)
