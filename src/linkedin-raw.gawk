#! /bin/gawk -f

function parseStart() {
	return match($0, /<div class="mb-1.5 flex flex-row">/, gg)
}

function parseImg() {
	return match($0, /<img.*?data-delayed-url="([^"]+)".*?>/, gg)
}

function parseTitle() {
	return match($0, /<h2.*?>([^<]+)</, gg)
}

function parseText() {
	return match($0, /<p.*?>(.+)(<\/p>)?/, gg)
}

function parseStop() {
	return match($0, /<div class="content-hub-tagged-topics/, gg)
}

{
	if (parseStart()) {
		print "---"
	}
	else if (parseImg()) {
		print "IMG: " gg[1]
	}
	else if (parseTitle()) {
		print "TIT: " gg[1]
	}
	else if (parseText()) {
		print "TXT: " gg[1]
	}
	else if (parseStop()) {
		print "---\n"
	}
	# else {
	# 	print ""
	# 	print $0
	# 	print ""
	# }
}

END {
	print ""
	exit


	ok = match($0,
/.*"id":"([0-9]+)"\
,"__typename":"([^"]+)"\
,"(title|url|name)":"([^"]+)"\
(,"(title|url)":"([^"]+)")?/, gg)

	if (ok)
	{
		printf "[%s] (%d)\n", gg[2], gg[1]
		printf "[%s] (%s)\n", gg[3], gg[4]
		if (gg[6]) printf "[%s] (%s)\n", gg[6], gg[7]
	}
	else
	{
		ok = match($0, /"authors":\[({"__ref":"Author:([0-9]+)"},?)+\]/, gg)

		if (ok)
		{
			printf "[Aref] (%d)\n", gg[2]
		}
		else
		{
			# "topic":{"__ref":"Topic:21"'
			ok = match($0, /"topic":{"__ref":"Topic:([0-9]+)"/, gg)

			if (ok) printf "[Tref] (%d)\n", gg[1]
			else print $0
		}
	}

	print ""
}
