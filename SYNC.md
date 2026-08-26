# Sync — Repo ↔ Paradox Mod Folder

Repo root = mod folder itself. Descriptor `maratha-empire.mod` at repo root maps to `Documents/Paradox Interactive/Hearts of Iron IV/mod/maratha-empire.mod` with `path="mod/maratha-empire"`.

## PowerShell (Windows)
```powershell
# repo → mod (after editing in repo)
.\sync.ps1

# mod → repo (if you edited via HOI4 launcher/tools directly in Paradox folder)
.\sync.ps1 -Reverse
```

## Alternate: symlink (live mirror, no copy)
```powershell
# Run as Admin
cmd /c mklink /D "C:\Users\zendrix\Documents\Paradox Interactive\Hearts of Iron IV\mod\maratha-empire" "C:\Users\zendrix\Documents\Programming\Dev\4weeksgrind\hoi4-modding\maratha-empire"
```

`sync.ps1` uses `robocopy /MIR` and preserves `descriptor.mod` → `maratha-empire.mod`.
