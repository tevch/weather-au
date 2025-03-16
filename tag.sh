if [ -z "$1" ]
        then
    echo "Usage tag <tag-name>"
    exit 1
fi

git tag $1

git push origin --tags
