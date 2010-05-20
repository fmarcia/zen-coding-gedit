my_zen_settings = {
    'css': {
		'snippets': {
			"css": " {\n${indentation}\n}",
		}
    },
	'html': {
		'abbreviations': {
			'jq': '<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>',
			'link:css': '<link rel="stylesheet" type="text/css" href="" media="all" />'
		},
		'snippets': {
			'dtdd': '<dt>${child}|</dt>\n<dd></dd>',
			'cdata': '<![CDATA[\n'
			         '${indentation}\n'
			         ']]>',
			'html:xt': '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n'
					'${indentation}"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n'
					'\n'
					'<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="${lang}">\n'
					'\n'
					    '${indentation}<head>\n'
					        '${indentation}${indentation}<meta http-equiv="Content-Type" content="text/html;charset=${charset}" />\n'
					        '${indentation}${indentation}<title></title>\n'
					        '${indentation}${indentation}\n'
					    '${indentation}</head>\n'
					    '\n'
					    '${indentation}<body>\n'
					        '${indentation}${indentation}${child}|\n'
					    '${indentation}</body>\n'
					'\n'
					'</html>'
		}
	}
}
