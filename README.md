Zen Coding for Gedit
====================

This plugin fully integrates [Zen Coding](http://code.google.com/p/zen-coding/) into [Gedit](http://projects.gnome.org/gedit/). With Zen Coding for Gedit, you can:

- Expand abbreviation
- Expand incrementally with abbreviation
- Wrap incrementally with abbreviation
- Select inward or outward (*)
- Merge lines
- Go to previous or next html tag (*)
- Go to previous or next html node (*)
- Go to previous or next edit point
- Update tag image size
- Toggle between image url and data
- Remove tag
- Split or join tags
- Toggle comment
- Create your own abbreviations and snippets
- Insert incrementally 'lorem ipsum' words or sentences, or random letters (**)

(*) these features use [html_navigation.py](http://github.com/fmarcia/zen-coding-gedit/blob/master/zencoding/html_navigation.py) instead of [zen_actions.py](http://github.com/fmarcia/zen-coding-gedit/blob/master/zencoding/zen_actions.py)

(**) see [lorem_ipsum.py](http://github.com/fmarcia/zen-coding-gedit/blob/master/zencoding/lorem_ipsum.py) for usage; this feature is not part of the original Zen Coding package.

These actions are available using keyboard shortcuts and menu items.

Installation
------------

1. Download [zip](http://github.com/fmarcia/zen-coding-gedit/zipball/master) or [tar](http://github.com/fmarcia/zen-coding-gedit/tarball/master) source
2. Unpack it
3. Run `./install.sh`
4. In Gedit, go to Edit > Preferences > Plugins and enable the plugin

Credits
-------

- Zen Coding is written by [Sergey Chikuyonok](http://chikuyonok.ru/)
- Zen Coding for Gedit is written by [Franck Marcia](http://github.com/fmarcia)

License
-------

Zen Coding for Gedit is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

