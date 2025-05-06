include_guard(GLOBAL)

include("${CMAKE_CURRENT_LIST_DIR}/python-integration-common.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/os_host_setup.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/../third_party/cmake-build-sys-utilities/scripts/build_sys_opts.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/../third_party/cmake-build-sys-utilities/scripts/logging.cmake")
    
set(PROJECT_BASE "${CMAKE_SOURCE_DIR}") #This SHOULD be set to the current project base

set(CHECK_IF_DEBUG_OUTPUT FALSE)
function(check_if_debug TARGET_NAME)
    set(CHECK_IF_DEBUG_OUTPUT FALSE PARENT_SCOPE)
    if("${CMAKE_BUILD_TYPE}" STREQUAL "Debug")
        set(CHECK_IF_DEBUG_OUTPUT TRUE PARENT_SCOPE)
        return()
    endif()

    set(temp "")
    set(get_prop_temp "")

    string(REGEX MATCH "^test_" temp "${TARGET_NAME}")
    if(NOT "${temp}" STREQUAL "" )
        set(CHECK_IF_DEBUG_OUTPUT TRUE PARENT_SCOPE)
        return()
    endif()
    set(temp "")

    get_property(get_prop_temp TARGET ${TARGET_NAME} PROPERTY extra_debug)
    if(get_prop_temp)
        set(CHECK_IF_DEBUG_OUTPUT TRUE PARENT_SCOPE)
        return()
    endif()

    if(NOT ${CMAKE_HOST_SYSTEM_NAME} STREQUAL "Windows")
    #C/CXX
        get_property(get_prop_temp TARGET ${TARGET_NAME} PROPERTY LANGUAGE)
        if(get_prop_temp STREQUAL "CXX")
            #Hello:
            get_property(get_prop_temp ${TARGET_NAME} PROPERTY COMPILE_OPTIONS)
            
            #If we are including symbols in the binary, we are probably intending to debug:
            string(REGEX MATCH "\s+-g\s+" temp "${get_prop_temp}") 
            if(NOT "${temp}" STREQUAL "")
                set(CHECK_IF_DEBUG_OUTPUT TRUE PARENT_SCOPE)
                return()
            endif()
        endif()
    else()
       message(FATAL_ERROR "Checking if the binary is to be a debug target is still a tad tricky in Windows.")
    endif()
    return()
endfunction()

#This is NOT going to work as-is due to source file properties not being inherited.
#What can we do about this?.
set(TARGET_LANGUAGE "")
function (get_target_language TARGET_NAME)
    unset(TARGET_LANGUAGE PARENT_SCOPE)
    set(language_retval "")
    set(get_prop_temp "")
    set(source_list "") 

    get_target_property(source_list "${TARGET_NAME}" SOURCES)
    foreach(source_file ${source_list})
        get_source_file_property(get_prop_temp "${source_file}" LANGUAGE)
        if("${get_prop_temp}" STREQUAL "NOTFOUND")
            continue()
        endif()
        if((NOT "${language_retval}" STREQUAL "") AND 
           (NOT "${get_prop_temp}" STREQUAL "${language_retval}"))
            message(FATAL_ERROR "Target \"${TARGET_NAME}\" has sources with different languages.")
        endif()
        set(language_retval "${get_prop_temp}")
    endforeach()

    if(NOT "${language_retval}" STREQUAL "")
        set(TARGET_LANGUAGE "${language_retval}" PARENT_SCOPE)
    endif()
    
endfunction()

set(BINARY_PATH "")
function(get_binary_path TARGET_NAME)
    # Get the output directory
    #Not sure if this is needed, but some funky stuff happened to me
    #to me once when I didn't unset a return variable once.
    unset(BINARY_PATH PARENT_SCOPE)
    get_target_property(binary_path ${TARGET_NAME} RUNTIME_OUTPUT_DIRECTORY)
    if(NOT binary_path)
        set(binary_path "${CMAKE_BINARY_DIR}")
    endif()
    
    # Get the binary name
    get_target_property(binary_name ${TARGET_NAME} OUTPUT_NAME)
    if(NOT binary_name)
        set(binary_name "${TARGET_NAME}")
    endif()
    
    # Handle multi-config builds (like Visual Studio)
    if(CMAKE_CONFIGURATION_TYPES)
        # For multi-config builds, we need to include the config type
        # We'll use the current build type or default to Debug
        if(CMAKE_BUILD_TYPE)
            set(config_type "${CMAKE_BUILD_TYPE}")
        else()
            set(config_type "Debug")
        endif()
        set(binary_path "${binary_path}/${config_type}/${binary_name}")
    else()
        # For single-config builds
        set(binary_path "${binary_path}/${binary_name}")
    endif()
    
    # Add extension for Windows
    if(WIN32)
        set(binary_path "${binary_path}.exe")
    endif()
    
    # Convert to absolute path
    get_filename_component(binary_path "${binary_path}" ABSOLUTE)
    set(BINARY_PATH "${binary_path}" PARENT_SCOPE)
endfunction()


#This will fail spectacularly if it is not a macro.
set(TARGET_RECORD_LIST "" CACHE STRING "List of target records." FORCE)
macro(register_target_info TARGET_NAME)
    set(get_prop_temp "")
    set(binary_path "")
    set(is_debug "false")
    set(target_record_temp "")
    set(target_rec_list "${TARGET_RECORD_LIST}")

    #Sanity checks:
    #Filter out executables and build the target record list.
    get_target_property(get_prop_temp ${TARGET_NAME} TYPE)
    if(get_prop_temp STREQUAL "EXECUTABLE")
        get_binary_path(${TARGET_NAME})
        set(binary_path "${BINARY_PATH}")
        unset(BINARY_PATH PARENT_SCOPE)
    else()
        #"extra_executable_path" is intended to mark techincally executable targets
        #(shell scripts, etc.).
        #It is not intended to mark executables that are not intended to be run.
        get_target_property(get_prop_temp ${TARGET_NAME} extra_executable_path)
        if(get_prop_temp STREQUAL "")
            log("Target ${TARGET_NAME} filtered out. Not an executable.")
            return()
        endif()    
    endif()

    check_if_debug(${TARGET_NAME})
    if(CHECK_IF_DEBUG_OUTPUT)
        set(is_debug "true")
    else()
        set(is_debug "false")
    endif()

    #Get the language of the target:
    get_target_language(${TARGET_NAME})
    if(NOT TARGET_LANGUAGE)
        message("Target \"${TARGET_NAME}\" does not have the LANGUAGES property set.")
    endif()
    set(target_record_temp "${TARGET_NAME},${binary_path},${TARGET_LANGUAGE},${is_debug}")
    list(APPEND target_rec_list "${target_record_temp}") 
    set(TARGET_RECORD_LIST "${target_rec_list}" CACHE STRING "List of target records." FORCE)
endmacro()

#This function will only regenerate the target list file
#if the list of targets has changed.
function(gen_target_list_file)
    set(get_prop_temp "")
    set(binary_path "")
    set(is_debug "false")
    set(target_record_temp "")
    set(target_record_list "")

    set(cmd_list "${python_cmd_list_template}")

    #Sanity checks:
    if(${ARGC} LESS 2)
        message(FATAL_ERROR "\"gen_target_list_file\": Too few arguments.")
    endif()
    
    if(${ARGC} GREATER 2)
        message(FATAL_ERROR "\"gen_target_list_file\": Too many arguments.")
    endif()
    
    set(oneValueArgs "OUTPUT_FILE")
    cmake_parse_arguments("gen_target_list_file" "" ${oneValueArgs} "" ${ARGN})
    
    if(NOT gen_target_list_file_OUTPUT_FILE)
        message(FATAL_ERROR "OUTPUT_FILE was not specified.")
    endif()

    #This script hashes its input and then checks the hash against
    #a set file under the ${CMAKE_BUILD_DIR} directory.
    list(APPEND cmd_list "${PYTHON_SCRIPT_DIR_PATH}/sha1-hash-args.py"
        "${gen_target_list_file_OUTPUT_FILE}"
        "${TARGET_RECORD_LIST}"
    )

    execute_process(
        COMMAND ${cmd_list}
        COMMAND_ECHO STDOUT
        WORKING_DIRECTORY "${PYTHON_SCRIPT_DIR_PATH}"
        COMMAND_ERROR_IS_FATAL ANY
    )
endfunction()
