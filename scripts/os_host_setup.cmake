include_guard(GLOBAL)

#Universal dependencies:
find_package(Python3)
#preliminary universal functions

function(find_dependency_program PROGRAM_NAME)
    find_program(PROGRAM_FOUND ${PROGRAM_NAME})
    if(PROGRAM_FOUND)
        set(PROGRAM_FOUND TRUE PARENT_SCOPE)
    endif()
endfunction()

function(look_for_dependency_program)
    unset(FOUND_ALTERNATIVE PARENT_SCOPE)
    list(LENGTH ARGN ARG_LEN_OUTPUT)
    if(ARG_LEN_OUTPUT LESS 1)
        message(FATAL_ERROR "No arguments passed.")
    endif()
    unset(FOUND_ALTERNATIVE)
    foreach(ALTERNATIVE ${ARGN})
        #find_dependency_program(${ALTERNATIVE})
	find_program(PROGRAM_FOUND ${ALTERNATIVE})
        if(PROGRAM_FOUND)
	    set(FOUND_ALTERNATIVE "${PROGRAM_FOUND}" PARENT_SCOPE)
    	    return()
        endif()
    endforeach()
endfunction()

#Host OS specific setup:
if(${CMAKE_HOST_SYSTEM_NAME} STREQUAL "Windows")
    #Dependencies
    look_for_dependency_program("powershell" "pwsh")
    if(NOT FOUND_ALTERNATIVE)
        message(FATAL_ERROR "PowerShell not found.")
    endif()
    set(POWERSHELL_COMMAND ${FOUND_ALTERNATIVE})

    function(echo_parameter_using_shell INPUT)
        set(ECHO_OUTPUT "")
        execute_process(
            COMMAND "${POWERSHELL_COMMAND}" "-c" "Write-Host" "'${INPUT}'"
            OUTPUT_VARIABLE ECHO_OUTPUT
            COMMAND_ERROR_IS_FATAL ANY
        )
        set(ECHO_OUTPUT "${ECHO_OUTPUT}" PARENT_SCOPE)
    endfunction()

elseif(${CMAKE_HOST_SYSTEM_NAME} STREQUAL "Darwin")

    look_for_dependency_program("sh")
    if(NOT FOUND_ALTERNATIVE)
        message(FATAL_ERROR "\"sh\" not found. Did you make changes to your PATH variable?")
    endif()

    function(echo_parameter_using_shell INPUT)
        set(ECHO_OUTPUT "")
        execute_process(
            COMMAND "sh" "-c" "\"echo '${INPUT}'\""
            OUTPUT_VARIABLE ECHO_OUTPUT
            COMMAND_ERROR_IS_FATAL ANY
        )
        set(ECHO_OUTPUT "${ECHO_OUTPUT}" PARENT_SCOPE)
    endfunction()

    elseif( ${CMAKE_HOST_SYSTEM_NAME} STREQUAL "Linux")

    look_for_dependency_program("echo")
    if(NOT FOUND_ALTERNATIVE)
        message(FATAL_ERROR "\"echo\" is not on the system PATH. Did you make changes to your PATH variable, or is this not a typical Linux distro.")
    endif()


    function(echo_parameter_using_shell INPUT)
        set(ECHO_OUTPUT "")
        execute_process(
            COMMAND "echo"  "'${INPUT}'"
            OUTPUT_VARIABLE ECHO_OUTPUT
            COMMAND_ERROR_IS_FATAL ANY
        )
        set(ECHO_OUTPUT "${ECHO_OUTPUT}" PARENT_SCOPE)
    endfunction()

else()
    message(FATAL_ERROR "\"${CMAKE_HOST_SYSTEM_NAME}\" is not a supported build host OS.")
endif()