#!/usr/bin/env python3
"""
Registry rebuild script for Agent 1 templates AND custom nodes.
Scans template and custom_nodes directories, reads metadata, and generates registry.json.
Works on Windows, macOS, and Linux.
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
import sys


def natural_sort_key(filename: str) -> Tuple:
    """
    Generate a sort key for natural sorting (1.jpg, 1a.png, 2.jpg, etc.)
    """
    match = re.match(r'^(\d+)([a-z]*)(\.[^.]+)$', filename.lower())
    if match:
        num, letters, ext = match.groups()
        return (int(num), letters, ext)
    return (float('inf'), filename.lower(), '')


def list_preview_frames(preview_dir: Path) -> List[str]:
    """
    List all preview images in a directory, sorted naturally.
    """
    if not preview_dir.exists():
        return []

    images = []
    for file in preview_dir.iterdir():
        if file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            images.append(file.name)

    images.sort(key=natural_sort_key)
    return images


def read_json_file(path: Path) -> Optional[Dict]:
    """Read and parse a JSON file. Returns None if invalid."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not read {path}: {e}", file=sys.stderr)
        return None


# ─── TEMPLATES ───────────────────────────────────────────────

def build_template_entry(template_dir: Path, metadata: Dict) -> Optional[Dict]:
    """Build a single template registry entry."""
    slug = metadata.get('slug')
    if not slug:
        print(f"Warning: Template in {template_dir} has no slug", file=sys.stderr)
        return None

    preview_dir = template_dir / 'preview'
    preview_frames = list_preview_frames(preview_dir)
    preview_path = f"templates/{slug}/preview/{preview_frames[0]}" if preview_frames else None

    return {
        'slug': slug,
        'name': metadata.get('name', slug),
        'description': metadata.get('description', ''),
        'author': metadata.get('author', 'Unknown'),
        'version': metadata.get('version', 1),
        'category': metadata.get('category', 'general'),
        'tags': metadata.get('tags', []),
        'techTags': metadata.get('techTags', []),
        'nodeCount': metadata.get('nodeCount', 0),
        'previewPath': preview_path,
        'templatePath': f"templates/{slug}/template.json",
        'previewFrames': preview_frames,
    }


def scan_templates(templates_dir: Path) -> List[Dict]:
    """Scan templates/ and build registry entries."""
    entries = []
    if not templates_dir.exists():
        return entries

    for item in sorted(templates_dir.iterdir()):
        if not item.is_dir() or item.name.startswith('.'):
            continue
        template_json = item / 'template.json'
        if not template_json.exists():
            continue
        metadata = read_json_file(template_json)
        if metadata:
            entry = build_template_entry(item, metadata)
            if entry:
                entries.append(entry)

    return entries


# ─── CUSTOM NODES ────────────────────────────────────────────

def build_node_entry(node_dir: Path, manifest: Dict, base_url: str) -> Optional[Dict]:
    """Build a single custom_nodes registry entry from its manifest.json."""
    node_id = manifest.get('id')
    if not node_id:
        print(f"Warning: Custom node in {node_dir} has no id", file=sys.stderr)
        return None

    is_core = manifest.get('isCore', False)
    version = manifest.get('version', '1.0.0')

    # Download URL: core nodes don't have one, community nodes point to GitHub Releases
    download_url = None
    if not is_core:
        download_url = manifest.get('downloadUrl',
            f"https://github.com/valsecchi75/agent1/releases/download/{node_id}-{version}/{node_id}.zip"
        )

    return {
        'id': node_id,
        'name': manifest.get('displayName', manifest.get('name', node_id)),
        'version': version,
        'author': manifest.get('author', 'Unknown'),
        'description': manifest.get('description', ''),
        'category': manifest.get('category', 'general'),
        'nodeCount': len(manifest.get('nodes', [])),
        'isCore': is_core,
        'removable': manifest.get('removable', not is_core),
        'downloadUrl': download_url,
        'manifestPath': f"custom_nodes/{node_id}/manifest.json",
        'size': manifest.get('size', 'specs-only' if is_core else 'unknown'),
    }


def scan_custom_nodes(custom_nodes_dir: Path, base_url: str) -> List[Dict]:
    """Scan custom_nodes/ and build registry entries."""
    entries = []
    if not custom_nodes_dir.exists():
        return entries

    for item in sorted(custom_nodes_dir.iterdir()):
        if not item.is_dir() or item.name.startswith('.'):
            continue
        manifest_path = item / 'manifest.json'
        if not manifest_path.exists():
            continue
        manifest = read_json_file(manifest_path)
        if manifest:
            entry = build_node_entry(item, manifest, base_url)
            if entry:
                entries.append(entry)

    return entries


# ─── MAIN ────────────────────────────────────────────────────

def bump_patch_version(version_str: str) -> str:
    """Bump the patch version of a semantic version string."""
    try:
        parts = version_str.split('.')
        if len(parts) >= 3:
            parts[2] = str(int(parts[2]) + 1)
            return '.'.join(parts[:3])
    except (ValueError, IndexError):
        pass
    return version_str


def main():
    """Main script entry point."""
    script_dir = Path(__file__).parent.absolute()
    templates_dir = script_dir / 'templates'
    custom_nodes_dir = script_dir / 'custom_nodes'
    registry_path = script_dir / 'registry.json'

    # Load existing registry for comparison
    existing = read_json_file(registry_path) or {}
    existing_template_slugs = {t['slug'] for t in existing.get('templates', [])}
    existing_node_ids = {p['id'] for p in existing.get('custom_nodes', [])}
    base_url = existing.get('baseUrl', 'https://raw.githubusercontent.com/valsecchi75/agent1/main')

    # Scan filesystem
    template_entries = scan_templates(templates_dir)
    node_entries = scan_custom_nodes(custom_nodes_dir, base_url)

    new_template_slugs = {t['slug'] for t in template_entries}
    new_node_ids = {p['id'] for p in node_entries}

    # Track changes
    templates_added = new_template_slugs - existing_template_slugs
    templates_removed = existing_template_slugs - new_template_slugs
    nodes_added = new_node_ids - existing_node_ids
    nodes_removed = existing_node_ids - new_node_ids

    has_changes = templates_added or templates_removed or nodes_added or nodes_removed

    # Build new registry
    version = existing.get('registryVersion', '2.0.0')
    if has_changes:
        version = bump_patch_version(version)

    new_registry = {
        'registryVersion': version,
        'updatedAt': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        'baseUrl': base_url,
        'templates': template_entries,
        'custom_nodes': node_entries,
    }

    # Write registry.json
    with open(registry_path, 'w', encoding='utf-8') as f:
        json.dump(new_registry, f, indent=2, ensure_ascii=False)

    # Print summary
    print("Registry rebuild complete!")
    print(f"  Version: {new_registry['registryVersion']}")
    print(f"  Templates: {len(template_entries)}")
    print(f"  Custom nodes: {len(node_entries)}")

    if templates_added:
        print(f"  Templates added: {', '.join(sorted(templates_added))}")
    if templates_removed:
        print(f"  Templates removed: {', '.join(sorted(templates_removed))}")
    if nodes_added:
        print(f"  Nodes added: {', '.join(sorted(nodes_added))}")
    if nodes_removed:
        print(f"  Nodes removed: {', '.join(sorted(nodes_removed))}")
    if not has_changes:
        print("  No changes detected")

    return 0


if __name__ == '__main__':
    sys.exit(main())
