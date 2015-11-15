Changelog
=========

0.3 (unreleased)
----------------

- Configuration is now stored in one fti attribute to avoid a field name erases an existing fti attribute.
  [sgeulette]
- Add a related field to store a text configuration that will be used to set related objects local roles.
  [sgeulette]
- Add memoize on localroles fields list
  [sgeulette]
- Change related local roles on transition, on addition, on removal, on moving, on configuration changes
  [sgeulette]
- Unconfigure dexterity.localroles subscriber for ILocalRoleListUpdatedEvent
  [sgeulette]

0.2.1 (2015-06-02)
------------------

- Update Readme
  [sgeulette]


0.2 (2015-06-02)
----------------

- Avoid exception on site deletion.
  [sgeulette]

- Add single value local role field.
  [cedricmessiant]

- Also lookup behaviors when searching for local role fields.
  [cedricmessiant]


0.1 (2014-10-24)
----------------

- Initial release
  [mpeeters]
