#!/bin/sh

#Locate project base:
echo "this_file: $0"
script_dir="$(realpath $(dirname $0))"
echo "script_dir: $script_dir"
#Import development-shell-helpers for POSIX shells:
dir="$script_dir"
while [ ! -e "$dir/LICENSE" ]; do
    dir="$(dirname $dir)"
done
dev_shell_helper_dir="$dir/third_party/development_shell_helpers/imports/posix_shell/Universal"
. "$dev_shell_helper_dir/repo_utils.sh"

#By default, this script uses the system-wide text-to-byte encoding.

TEMP_FILE_NAME="sha1test_XXXXXX"
TEMP_FILE_PATH=""
FILE_DIR=""
SAMPLE_TARGET_LIST_FILE="$script_dir/raw_sample_target_list.txt"
if [ ! -e "$SAMPLE_TARGET_LIST_FILE" ]; then
    Write_RepoCorruptMessage
    exit 1
fi


if [ ! -e "$script_dir/sample_file_name.txt" ]; then
    Write_RepoCorruptMessage
    exit 1  
fi

SAMPLE_FILE_NAME="$(cat $script_dir/sample_file_name.txt)"

TEMP_FILE_PATH=$(mktemp $TEMP_FILE_NAME)

    

#Read in list of targets, sort it, and convert uppercase to lowercase:
cat $SAMPLE_TARGET_LIST_FILE | sort | tr '[:upper:]' '[:lower:]' > $TEMP_FILE_PATH

#Calculate the hash:
HASH="$(sha1sum $TEMP_FILE_PATH | awk '{print $1}')"

#Write hash and sorted list to output file
echo "$HASH" > $SAMPLE_FILE_NAME
cat $TEMP_FILE_PATH >> $SAMPLE_FILE_NAME

#Remove temp file:
rm -rf $TEMP_FILE_PATH