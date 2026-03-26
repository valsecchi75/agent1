# AGENT 1 — Registry

Remote registry for the **AGENT 1** node-based creative generation platform.

Contains both **workflow templates** and **node packs** that users can browse and install from the app.

## Structure

```
agent1-registry/
  registry.json                    # Main index (fetched by the app)
  rebuild_registry.py              # Auto-rebuild script
  PUSH_TO_GITHUB.bat               # Windows: rebuild + commit + push

  templates/                       # Workflow templates
    {slug}/
      template.json                # Full workflow data (nodes, edges, metadata)
      preview/
        1.jpg                      # Primary preview image
        1a.jpg                     # Animation frame (optional)

  custom_nodes/                    # Node packages (same structure as app/custom_nodes/)
    .template/                     # Starter template for new nodes
    agent1-foundation/             # Core nodes (specs-only, not removable)
      manifest.json
      specs/                       # node-spec.json files (for RAG)
      README.md
    neural-atelier/                # Community/custom node package
      manifest.json
      specs/
      README.md
    {new-node-pack}/               # Add new node packages here
      manifest.json
      specs/
      README.md
```

## How it works

1. The app fetches `registry.json` from this repo
2. **Template Explorer** shows available workflow templates with previews
3. **Node Manager** shows available custom nodes with install/update buttons
4. When the user installs a node package, the app downloads the .zip from GitHub Releases
5. Node package is extracted to `custom_nodes/{node-id}/`
6. RAG index (`_index.json`) is auto-regenerated

## Registry URL

```
https://raw.githubusercontent.com/valsecchi75/agent1/main/registry.json
```

## Quick publish workflow

### Adding a template
1. Create `templates/{slug}/template.json` + `preview/` images
2. Run `PUSH_TO_GITHUB.bat` (or `python rebuild_registry.py` + git push)

### Adding a custom node package
1. Copy `custom_nodes/.template/` to `custom_nodes/{node-id}/`
2. Edit `manifest.json` with your pack info and nodes
3. Add `node-spec.json` files in `specs/` for each node
4. Create a GitHub Release with the `.zip` of your pack
5. Run `PUSH_TO_GITHUB.bat`

### Updating an existing node package
1. Update `manifest.json` version
2. Create new GitHub Release with the updated `.zip`
3. Run `PUSH_TO_GITHUB.bat`

## Template format

```json
{
  "version": 1,
  "slug": "my-template",
  "name": "My Template",
  "description": "What this template does",
  "author": "Your Name",
  "category": "simple|advanced|production|experimental",
  "tags": ["custom", "tags"],
  "techTags": ["Nano Banana", "LLM"],
  "nodes": [...],
  "edges": [...]
}
```

## Custom node manifest format

```json
{
  "id": "my-pack",
  "name": "My Pack",
  "displayName": "My Pack Display Name",
  "version": "1.0.0",
  "author": "Author Name",
  "description": "Short description",
  "category": "image|video|audio|3d|llm|utility",
  "minAppVersion": "0.8.0",
  "nodes": [
    {
      "type": "myNode",
      "name": "My Node",
      "category": "image/generation",
      "specFile": "specs/myNode.json"
    }
  ],
  "hasSpecs": true,
  "dependencies": []
}
```
