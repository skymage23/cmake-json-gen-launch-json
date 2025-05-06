include_guard(GLOBAL)

define_property(TARGET PROPERTY extra_language
    BRIEF_DOCS "Programming language of target. Extends CMake support."
    FULL_DOCS "Programming language of target. Used for languages that CMake doesn't natively support."
)
set(EXTRA_LANGUAGES "")
list(APPEND EXTRA_LANGUAGES "Python")

set(EXTRA_LANGUAGES_EXTENSIONS "")
function(define_extra_lang_file_extensions)
    if(${ARGC} LESS 2)
        message(FATAL_ERROR "\"define_extra_lang_file_extensions\": Too many arguments.")
    endif()
    #Hello
    set(temp "")
    foreach(arg IN LISTS ARGN)
        set(temp "${temp},${arg}")
    endforeach()
    list(APPEND EXTRA_LANGUAGES_EXTENSIONS "${temp}")
    set(EXTRA_LANGUAGES_EXTENSIONS "${EXTRA_LANGUAGES_EXTENSIONS}" PARENT_SCOPE)
endfunction()

define_extra_lang_file_extenstions("Python" "py")

set(LANG_OUTPUT "")
#Add check for null later.
function(get_language_for_extension extension)
    #Hello
    set(LANG_OUTPUT "" PARENT_SCOPE)
    set(temp "")
    set(temp_len 0)
    set(language "")
    foreach(record in "${EXTRA_LANGUAGES_EXTENSIONS}")
        string(REPLACE ',' ';' temp ${record})
        list(LENGTH "${temp}" temp_len)
        math(EXPR temp_len "${temp_len} - 1")

        foreach(i RANGE 1 ${temp_len})
            list(GET "${record}" ${i} temp)
            if("${extension}" STREQUAL "${temp}")
                list(GET "${record}" 0 temp)
                set(LANG_OUTPUT "${temp}" PARENT_SCOPE)
                return()
            endif()
        endforeach
    endforeach()
    return()
endfunction()

define_property(TARGET PROPERTY extra_executable_path
    BRIEF_DOCS "Path to executable. Extends CMake support."
    FULL_DOCS "Path to executable. Used for targets where CMake cannot determine this value on its own."
)

define_property(TARGET PROPERTY extra_debug
    BRIEF_DOCS "Boolean. Debuggable? Extends CMake support"
    FULL_DOCS "Boolean. Sets whether or not this executable is to be debugged. Extends CMake support."
)