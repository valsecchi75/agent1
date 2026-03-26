================================================================================
AGENT 1 REGISTRY — REBUILD & PUBLISH GUIDE
================================================================================

This registry contains both WORKFLOW TEMPLATES and CUSTOM NODE PACKAGES.
The rebuild script scans both directories and generates registry.json.

================================================================================
QUICK PUBLISH (Windows)
================================================================================

Double-click PUSH_TO_GITHUB.bat
  -> Rebuilds registry.json from templates/ + custom_nodes/
  -> Commits and pushes to GitHub

================================================================================
MANUAL REBUILD
================================================================================

  python rebuild_registry.py

The script:
  1. Scans templates/{slug}/template.json -> template entries
  2. Scans custom_nodes/{pack-id}/manifest.json -> pack entries
  3. Skips directories starting with "." (like .template/)
  4. Auto-bumps version if templates or custom_nodes changed
  5. Prints change summary

================================================================================
ADDING A NEW CUSTOM NODE PACKAGE
================================================================================

  1. Copy custom_nodes/.template/ to custom_nodes/{your-pack-id}/
  2. Edit manifest.json with your pack info and nodes
  3. Add node-spec.json files in specs/ for each node
  4. Create a GitHub Release with the .zip of your pack
  5. Run PUSH_TO_GITHUB.bat (or rebuild + git push)

================================================================================
ADDING A NEW TEMPLATE
================================================================================

  1. Create templates/{slug}/template.json
  2. Add preview images in templates/{slug}/preview/
  3. Run PUSH_TO_GITHUB.bat

================================================================================
REGISTRY.JSON STRUCTURE (v2.0)
================================================================================

{
  "registryVersion": "2.0.x",
  "updatedAt": "ISO timestamp",
  "baseUrl": "https://raw.githubusercontent.com/valsecchi75/agent1/main",
  "templates": [
    { "slug", "name", "description", "author", "version", "category",
      "tags", "techTags", "nodeCount", "previewPath", "templatePath",
      "previewFrames" }
  ],
  "custom_nodes": [
    { "id", "name", "version", "author", "description", "category",
      "nodeCount", "isCore", "removable", "downloadUrl", "manifestPath",
      "size" }
  ]
}

================================================================================
PREVIEW IMAGE SORTING
================================================================================

Preview images are sorted naturally:
  Input:  1a.jpg, 1.jpg, 2.jpg, 1b.png
  Output: 1.jpg, 1a.jpg, 1b.png, 2.jpg

Supported formats: jpg, jpeg, png, gif, webp

================================================================================
CROSS-PLATFORM
================================================================================

Python script: Works on Windows, macOS, Linux (pathlib + UTF-8)
Windows .bat: Pure ASCII, setlocal enabledelayexpansion, >nul redirection

================================================================================
