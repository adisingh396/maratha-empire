param([switch]$Reverse)
$repo = $PSScriptRoot
$modFolder = "$env:USERPROFILE\Documents\Paradox Interactive\Hearts of Iron IV\mod\maratha-empire"
$modFile = "$env:USERPROFILE\Documents\Paradox Interactive\Hearts of Iron IV\mod\maratha-empire.mod"
$repoMod = Join-Path $repo "maratha-empire.mod"
$repoDescriptor = Join-Path $repo "descriptor.mod"
if ($Reverse) {
    Write-Host "Syncing Paradox mod → repo..."
    if (Test-Path $modFolder) { robocopy $modFolder $repo /E /NFL /NDL /NJH /NJS /R:0 /W:0 /XD .git | Out-Null }
    if (Test-Path $modFile) { Copy-Item $modFile -Destination $repoMod -Force; Copy-Item $modFile -Destination $repoDescriptor -Force }
    Write-Host "Done (mod → repo)"
} else {
    Write-Host "Syncing repo → Paradox mod..."
    New-Item -ItemType Directory -Force -Path $modFolder | Out-Null
    robocopy $repo $modFolder /E /NFL /NDL /NJH /NJS /R:0 /W:0 /XD .git /XF *.ps1 SYNC.md | Out-Null
    if (Test-Path $repoMod) { Copy-Item $repoMod -Destination $modFile -Force }
    elseif (Test-Path $repoDescriptor) { Copy-Item $repoDescriptor -Destination $modFile -Force }
    Write-Host "Done (repo → mod) to $modFolder"
}
