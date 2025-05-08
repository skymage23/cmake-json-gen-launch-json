#cat target_list.txt | sort
echo "Shell script hashing these lines:" >&2
{
    cat target_list.txt | sort | while read -r line; do
        # Strip whitespace and newlines from each line
        stripped_line=$(echo "$line" | tr -d '\r\n' | sed 's/^[[:space:]]*//g;s/[[:space:]]*$//g')
        # Debug output
        echo "  '$stripped_line' -> $(echo -n "$stripped_line" | xxd -p)" >&2
        # Output the stripped line
        echo -n "$stripped_line"
    done
} | sha1sum -b | awk '{print $1}'
