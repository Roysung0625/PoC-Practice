# Compatibility entry point for existing local installations.
param([string]$AdminSecret = '', [string]$Database = 'poc_idempiere')
$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
& (Join-Path $root 'product-registration/database/Setup.ps1') @PSBoundParameters
