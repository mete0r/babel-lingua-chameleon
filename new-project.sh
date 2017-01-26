#!/bin/sh

set -e

PROJECT=$1
SUMMARY=$2
PACKAGE=$3

if [ -z "$PROJECT" ]; then
	echo "usage: $0 <PROJECT> <SUMMARY> [<PACKAGE>]"
	exit 1
fi

if [ -z "$SUMMARY" ]; then
	echo "usage: $0 <PROJECT> <SUMMARY> [<PACKAGE>]"
	exit 1
fi

if [ -z "$PACKAGE" ]; then
	PACKAGE=$PROJECT
fi

rm -rf $PACKAGE
git mv METE0R_PACKAGE $PACKAGE
git grep --name-only METE0R_PACKAGE | xargs sed -i -e "s/METE0R_PACKAGE/$PACKAGE/g"
git grep --name-only METE0R-PROJECT | xargs sed -i -e "s/METE0R-PROJECT/$PROJECT/g"
git grep --name-only SOME_DESCRIPTION | xargs sed -i -e "s/SOME_DESCRIPTION/$SUMMARY/g"
find . -name 'METE0R-PROJECT.*' -exec bash -c "mv \$0 \${0/METE0R-PROJECT/$PROJECT}" {} \;
git add $PACKAGE
git status --porcelain | grep '^ M' | cut -b 4- | xargs git add
git rm -f new-project.sh
git commit -m "$PROJECT: initial commit"
