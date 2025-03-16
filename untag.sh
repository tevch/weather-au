if [ -z "$1" ]
	then
		echo "Usage tag <tag-name>"
	        exit 1
	fi

git tag -d $1
git push origin :refs/tags/$1
