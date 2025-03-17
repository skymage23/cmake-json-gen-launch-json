#!/usr/bin/pwsh
Import-Module -Name "../../../../third_party/development_shell_helpers/imports/PowerShell/Universal/repo_utils.psm1"
Import-Module -Name "../../../../third_party/development_shell_helpers/imports/PowerShell/Specific/ps-utils.psm1"

function Get-SampleDirPath {
    $curr_file = $PSScriptRoot
    return $curr_file
}

function Get-SampleFileName {
    param(
        [Parameter(Mandatory=$true)]
        [string]$sample_file_path
    )
    [string[]]$lines = $null
    $filepath = Join-Path -Path $sample_dir_path -ChildPath "sample_file_name.txt"
    if ( -not (Test-Path -Path $sample_file_path)){
        Write-RepoCorruptMessage
        return $null
    }

    $lines = Get-Content -Path $filepath
    if($lines.Length -lt 1){
        Write-RepoCorruptMessage
        return $null
    }
    return Join-Path -Path $sample_dir_path -ChildPath $lines[0]
}


function Get-SampleTargetList {
    param(
        [Parameter(Mandatory=$true)]
        [string]$sample_dir_path
    )
    $filepath = Join-Path -Path $sample_dir_path -ChildPath "raw_sample_target_list.txt"

    if (-not (Test-Path -Path $filepath)){
         Write-RepoCorruptMessage
         return $null
    }
    [string[]]$lines = Get-Content -Path $filepath -Encoding utf8
    #$content = Get-Content -Path $filepath -AsByteStream -Raw

    if($lines.Length -le 0){
        Write-RepoCorruptMessage
        return $null
    }
    
    for( $i = 0; $i -lt $lines.Length; $i++){
        $lines[$i] = $lines[$i].ToLower()
    }
    return $lines
}

function Get-HashForTargetList {
    [OutputType([String])]
    param(
        [Parameter(Mandatory=$true)]
        [string[]] $target_list
    )
    $str_builder =  New-Object -TypeName "System.Text.StringBuilder"
    $byte_hash = $null
    $data_blob = [Byte[]]
    $text_encoder = New-Object -TypeName "System.Text.UTF8Encoding" $false
    
    [System.Array]::Sort($target_list)
    foreach($str in $target_list){
        $null = $str_builder.Append($str.Trim())
    } 
    $data_blob = $text_encoder.GetBytes($str_builder.ToString())
    Use-InThisBlockOnly([System.Security.Cryptography.SHA1]::Create()){
        param(
            [System.Security.Cryptography.SHA1]$hasher
        )

        #If you see a red underline undeneath "byte_hash", ignore it.
        #That's just the editor complaining that it doesn't see
        #the variable being used inside what it thinks is a new scope.
        #In actuality, this script block is executed inside the scope
        #of the parent function.
        $byte_hash = $hasher.ComputeHash($data_blob)
    }

    $null = $str_builder.Clear()
    foreach($byte in $byte_hash){
        $null = $str_builder.Append($byte.ToString("x2"))
    }
    return $str_builder.ToString()
}


#Doing the writes this way ensures we are writing using UTF-8 with no BOM.
function Write-TargetListFileWithHash {
    param(
        [Parameter(Mandatory=$true)]
        [string]$filepath,
        [Parameter(Mandatory=$true)]
        [string]$hash,
        [Parameter(Mandatory=$true)]
        [string[]]$target_list
    )
         $encoder = New-Object -TypeName "System.Text.UTF8Encoding" $false 
         $fileStream = $null
         $streamWriter = $null

         $newFile = New-Item -Force -Path $(Split-Path -Path $filepath -Parent) -Name $(Split-Path -Path $filepath -Leaf)
         try {
             $fileStream = $newFile.OpenWrite()
             $streamWriter = [System.IO.BinaryWriter]::new($fileStream)
             
             #Write stuff
             $streamWriter.Write($encoder.GetBytes("{0}`n" -f $hash))
             foreach($item in $target_list){
                 $streamWriter.Write($encoder.GetBytes("{0}`n" -f $item))
             }
         }
         finally {
             $streamWriter.Dispose()
             $fileStream.Dispose()
         }
}



function main {
    $sample_dir_path = Get-SampleDirPath
    if($null -eq $sample_dir_path){
        exit
    }

    $file_with_hash_filename = Get-SampleFileName $sample_dir_path
    if($null -eq $file_with_hash_filename){
        exit
    }
    
    $target_list = $(Get-SampleTargetList -sample_dir_path $sample_dir_path) | Sort-Object
    if ($null -eq $target_list) {
        exit
    }
    $hash = Get-HashForTargetList -target_list $target_list
    Write-TargetListFileWithHash -filepath $file_with_hash_filename -hash $hash -target_list $target_list
}

main