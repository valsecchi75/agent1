# AGENT 1 Foundation Nodes

> Core built-in nodes that ship with every AGENT 1 installation.

This is a **specs-only** pack — the node code lives in `app/src/`. This pack provides `node-spec.json` files that power the RAG prompt-to-workflow system.

## Nodes (26)

| Node | Type | Category | Description |
|------|------|----------|-------------|
| Image Input | imageInput | input | Load images from file, URL, or clipboard |
| Audio Input | audioInput | input | Load audio files for processing |
| Annotation | annotation | input | Add notes and comments to workflow |
| Prompt | prompt | input | Text prompt with variables and templates |
| Array | array | utility | Split text into array items with delimiter/regex |
| Prompt Constructor | promptConstructor | llm/utility | Build complex prompts from parts with @variables |
| Nano Banana | nanoBanana | image/generation | AI image generation via Nano Banana API |
| Generate Video | generateVideo | video/generation | AI video generation via Veo 3.1 |
| Generate Audio | generateAudio | audio/generation | AI audio/music generation |
| Generate 3D | generate3d | 3d/generation | AI 3D model generation |
| LLM Generate | llmGenerate | llm | Text generation via Gemini, Claude, GPT |
| Split Grid | splitGrid | image/utility | Split image into grid cells for parallel processing |
| Output | output | output | Final workflow output node |
| Output Gallery | outputGallery | output | Collect multiple outputs in a gallery |
| Image Compare | imageCompare | image/utility | Side-by-side image comparison |
| Video Stitch | videoStitch | video/utility | Combine video clips with transitions |
| Ease Curve | easeCurve | video/utility | Easing curves for video transitions |
| Video Trim | videoTrim | video/utility | Trim video clips |
| Video Frame Grab | videoFrameGrab | video/utility | Extract frames from video |
| Router | router | flow/routing | Route data to multiple outputs |
| Switch | switch | flow/routing | Conditional data routing |
| Conditional Switch | conditionalSwitch | flow/routing | Rule-based conditional routing |
| GLB Viewer | glbViewer | 3d/utility | View and interact with 3D models |
| Preview Image | previewImage | utility/display | Simple image preview with pass-through output |
| Show Anything | showAnything | utility/display | Universal preview — auto-detects image, text, video, audio, JSON |
| Morpheus Model Management | morpheusModelManagement | custom/morpheus | Browsable digital talent catalog with Patreon auth |

## This pack cannot be disabled or removed.
