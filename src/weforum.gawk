#! /bin/gawk -f

BEGIN {
	# system("make test_weforum_grammars")
	# exit
}

function parseArAuTo() {
	return match($0,
/.*"id":"([0-9]+)"\
,"__typename":"([^"]+)"\
,"(title|url|name)":"([^"]+)"\
(,"(title|url)":"([^"]+)")?/, gg)
}

function parseAuRefs() {
	return match($0, /"authors":\[({"__ref":"Author:([0-9]+)"},?)+\]/, gg)
}

function parseToRef() {
	return match($0, /"topic":{"__ref":"Topic:([0-9]+)"/, gg)
}

function parseDat() {
	return match($0, /"publishedAt":"(.+)"/, gg)
}

function parseDes() {
	return match($0, /"description":"(.+)"/, gg)
}

{
	if (parseArAuTo()) {
		print ""
		printf "[%s] (%d)\n", gg[2], gg[1]
		printf "[%s] (%s)\n", gg[3], gg[4]
		if (gg[6]) printf "[%s] (%s)\n", gg[6], gg[7]
	}
	else if (parseAuRefs()) {
		print ""
		printf "[Aref] (%d)\n", gg[2]
	}
	else if (parseToRef()) {
		print ""
		printf "[Tref] (%d)\n", gg[1]
	}
	else if (parseDat()) {
		print ""
		printf "[Dat] (%s)\n", gg[1]
	}
	else if (parseDes()) {
		print ""
		printf "[Des] (%s)\n", gg[1]
	}
	else {
		print ""
		print $0
		print ""
	}
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