#  Zen Coding for Gedit
#
#  Copyright (C) 2010 Franck Marcia
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
Connexion of Zen Coding to Gedit

@author Franck Marcia (franck.marcia@gmail.com)
@link http://github.com/fmarcia/zen-coding-gedit
'''

import gedit, gobject, gtk, os

from zen_editor import ZenEditor

zencoding_ui_str = """
<ui>
  <menubar name="MenuBar">
    <menu name="EditMenu" action="Edit">
      <placeholder name="EditOps_5">
        <menu action="ZenCodingMenuAction">
          <menuitem name="ZenCodingExpand"   action="ZenCodingExpandAction"/>
          <menuitem name="ZenCodingExpandW"  action="ZenCodingExpandWAction"/>
          <menuitem name="ZenCodingWrap"     action="ZenCodingWrapAction"/>
          <separator/>
          <menuitem name="ZenCodingInward"   action="ZenCodingInwardAction"/>
          <menuitem name="ZenCodingOutward"  action="ZenCodingOutwardAction"/>
          <separator/>
          <menuitem name="ZenCodingPTag"     action="ZenCodingPTagAction"/>
          <menuitem name="ZenCodingNTag"     action="ZenCodingNTagAction"/>
          <menuitem name="ZenCodingPNode"    action="ZenCodingPNodeAction"/>
          <menuitem name="ZenCodingNNode"    action="ZenCodingNNodeAction"/>
          <menuitem name="ZenCodingPrev"     action="ZenCodingPrevAction"/>
          <menuitem name="ZenCodingNext"     action="ZenCodingNextAction"/>
          <separator/>
          <menuitem name="ZenCodingSize"     action="ZenCodingSizeAction"/>
          <menuitem name="ZenCodingData"     action="ZenCodingDataAction"/>
          <separator/>
          <menuitem name="ZenCodingMerge"    action="ZenCodingMergeAction"/>
          <menuitem name="ZenCodingRemove"   action="ZenCodingRemoveAction"/>
          <menuitem name="ZenCodingSplit"    action="ZenCodingSplitAction"/>
          <menuitem name="ZenCodingComment"  action="ZenCodingCommentAction"/>
          <separator/>
          <menuitem name="ZenCodingSettings" action="ZenCodingSettingsAction"/>
        </menu>
        <menuitem   name="LoremIpsum"        action="LoremIpsumAction"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

class ZenCodingPlugin(gedit.Plugin):
    """A Gedit plugin to implement Zen Coding's HTML and CSS shorthand expander."""

    def activate(self, window):
        actions = [
          ('ZenCodingMenuAction',     None, '_Zen Coding',                  None,                "Zen Coding tools",                            None),
          ('ZenCodingExpandAction',   None, '_Expand abbreviation',         '<Ctrl>E',            "Expand abbreviation to raw HTML/CSS",         self.expand_abbreviation),
          ('ZenCodingExpandWAction',  None, 'E_xpand with abbreviation...', '<Ctrl><Alt>E',       "Type in an abbreviation to expand",           self.expand_with_abbreviation),
          ('ZenCodingWrapAction',     None, '_Wrap with abbreviation...',   '<Ctrl><Shift>E',     "Wrap with code expanded from abbreviation",   self.wrap_with_abbreviation),
          ('ZenCodingInwardAction',   None, 'Select _inward',               '<Ctrl><Alt>I',       "Select inner tag's content",                  self.match_pair_inward),
          ('ZenCodingOutwardAction',  None, 'Select _outward',              '<Ctrl><Alt>O',       "Select outer tag's content",                  self.match_pair_outward),
          ('ZenCodingPTagAction',     None, 'Previous tag',                 '<Ctrl><Alt>Up',      "Select the previous tag in HTML code",        self.prev_tag),
          ('ZenCodingNTagAction',     None, 'Next tag',                     '<Ctrl><Alt>Down',    "Select the next tag in HTML code",            self.next_tag),
          ('ZenCodingPNodeAction',    None, 'Previous node',                '<Ctrl><Alt>Left',    "Select the previous HTML node",               self.prev_node),
          ('ZenCodingNNodeAction',    None, 'Next node',                    '<Ctrl><Alt>Right',   "Select the next HTML node",                   self.next_node),
          ('ZenCodingPrevAction',     None, '_Previous edit point',         '<Alt>Left',          "Place the cursor at the previous edit point", self.prev_edit_point),
          ('ZenCodingNextAction',     None, '_Next edit point',             '<Alt>Right',         "Place the cursor at the next edit point",     self.next_edit_point),
          ('ZenCodingSizeAction',     None, 'Update image _size',           '<Ctrl><Alt>S',       "Update image size tag from file",             self.update_image_size),
          ('ZenCodingDataAction',     None, 'Toggle image url/da_ta',       '<Ctrl><Alt>A',       "Toggle between image url and data",           self.encode_decode_base64),
          ('ZenCodingMergeAction',    None, '_Merge lines',                 '<Ctrl><Alt>M',       "Merge all lines of the current selection",    self.merge_lines),
          ('ZenCodingRemoveAction',   None, '_Remove tag',                  '<Ctrl><Alt>R',       "Remove a tag",                                self.remove_tag),
          ('ZenCodingSplitAction',    None, 'Split or _join tag',           '<Ctrl><Alt>J',       "Toggle between single and double tag",        self.split_join_tag),
          ('ZenCodingCommentAction',  None, 'Toggle _comment',              '<Ctrl><Alt>C',       "Toggle an XML or HTML comment",               self.toggle_comment),
          ('ZenCodingSettingsAction', None, 'E_dit settings...',            None,                "Customize snippets and abbreviations",        self.edit_settings),
          ('LoremIpsumAction',        None, 'Lorem ipsum...',               '<Ctrl><Alt>X',       "Insert a lorem ipsum string",                 self.lorem_ipsum)
        ]
        windowdata = dict()
        window.set_data("ZenCodingPluginDataKey", windowdata)
        windowdata["action_group"] = gtk.ActionGroup("GeditZenCodingPluginActions")
        windowdata["action_group"].add_actions(actions, window)
        manager = window.get_ui_manager()
        manager.insert_action_group(windowdata["action_group"], -1)
        windowdata["ui_id"] = manager.add_ui_from_string(zencoding_ui_str)
        window.set_data("ZenCodingPluginInfo", windowdata)
        self.editor = ZenEditor()
        error = self.editor.get_user_settings_error()
        if error:
            md = gtk.MessageDialog(window, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR,
                gtk.BUTTONS_CLOSE, "There is an error in user settings:")
            message = "{0} on line {1} at character {2}\n\nUser settings will not be available."
            md.set_title("Zen Coding error")
            md.format_secondary_text(message.format(error['msg'], error['lineno'], error['offset']))
            md.run()
            md.destroy()

    def deactivate(self, window):
        windowdata = window.get_data("ZenCodingPluginDataKey")
        manager = window.get_ui_manager()
        manager.remove_ui(windowdata["ui_id"])
        manager.remove_action_group(windowdata["action_group"])

    def update_ui(self, window):
        view = window.get_active_view()
        windowdata = window.get_data("ZenCodingPluginDataKey")
        windowdata["action_group"].set_sensitive(bool(view and view.get_editable()))

    def expand_abbreviation(self, action, window):
        self.editor.expand_abbreviation(window)
        
    def expand_with_abbreviation(self, action, window):
        self.editor.expand_with_abbreviation(window)

    def wrap_with_abbreviation(self, action, window):
        self.editor.wrap_with_abbreviation(window)

    def match_pair_inward(self, action, window):
        self.editor.match_pair_inward(window)

    def match_pair_outward(self, action, window):
        self.editor.match_pair_outward(window)

    def merge_lines(self, action, window):
        self.editor.merge_lines(window)

    def prev_tag(self, action, window):
        self.editor.prev_tag(window)

    def next_tag(self, action, window):
        self.editor.next_tag(window)

    def prev_node(self, action, window):
        self.editor.prev_node(window)

    def next_node(self, action, window):
        self.editor.next_node(window)

    def prev_edit_point(self, action, window):
        self.editor.prev_edit_point(window)

    def next_edit_point(self, action, window):
        self.editor.next_edit_point(window)

    def update_image_size(self, action, window):
        self.editor.update_image_size(window)

    def encode_decode_base64(self, action, window):
        self.editor.encode_decode_base64(window)

    def remove_tag(self, action, window):
        self.editor.remove_tag(window)

    def split_join_tag(self, action, window):
        self.editor.split_join_tag(window)

    def toggle_comment(self, action, window):
        self.editor.toggle_comment(window)

    def edit_settings(self, action, window):
        window.create_tab_from_uri("file:///" + os.path.expanduser("~/.gnome2/gedit/plugins/zencoding/my_zen_settings.py"), None, 0, True, True)

    def lorem_ipsum(self, action, window):
        self.editor.lorem_ipsum(window)

