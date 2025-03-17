#!/bin/sh
#LOCALE

function print_err {
    echo >&2 "$1"
}

function die {
    print_err $1
    exit 1
}

#Try to force UTF-8 with no BOM
old_LOCALE=""
UTF8_LOCALE="en_US.UTF-8"
UTF8_LOCALE_REGEX="en_US\.UTF-8"

if [ "$(echo "$LANG" | awk -c '$1~/UTF-8/ {print $1}')" == "" ]; then
    echo "We need to try to change the locale."
    if which localectl 2>&1 >/dev/null; then
        if ! `sudo localectl list-locales | awk -c "\$1~/$UTF8_LOCALE_REGEX/{print \$1}"`; then
            die "The $UTF8_LOCALE locale is not installed or configured on this system."            
        fi

        old_locale="$LANG"
        ! sudo localectl set-locale "UTF8_LOCALE" && die "Unable to set locale to UTF8_LOCALE"

    else
        echo "This is not a SystemD-based distro. We will TRY our best"
        echo "to ensure this script works correctly, but we cannot guarantee it."
        echo "Welcome to the world of UNIX-like OSs, where developer ideological"
        echo "differences manifest as imcompatibilities."

        old_locale="$LANG"
        export LANG="$UTF8_LOCALE"
    fi
fi

##Locate project base:
script_dir="$(realpath $(dirname $0))"
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

TEMP_FILE_PATH="$(mktemp $TEMP_FILE_NAME)"

    

#Read in list of targets, sort it, and convert uppercase to lowercase:
PRINT_PROCESSED_INPUT="$(cat $SAMPLE_TARGET_LIST_FILE | tr '[:upper:]' '[:lower:]' | sort)"
echo "$PRINT_PROCESSED_INPUT" | tr -d \\n > $TEMP_FILE_PATH

#Calculate the hash:
HASH="$(sha1sum $TEMP_FILE_PATH | awk '{print $1}')"

#Write hash and sorted list to output file
echo "$HASH" > $SAMPLE_FILE_NAME
echo "$PRINT_PROCESSED_INPUT" >> $SAMPLE_FILE_NAME

#Remove temp file:
rm -rf $TEMP_FILE_PATH


if [ "$old_LOCALE" != "" ] ; then 
    if which localectl 2>&1 >/dev/null; then
        ! sudo localectl set-locale "$old_LOCALE" && die "Unable to set locale to back to $old_LOCALE"

    else
        export LANG="$old_LOCALE"
    fi
fi