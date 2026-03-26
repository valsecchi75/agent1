# AGENT 1 Foundation Nodes

> Core built-in nodes that ship with every AGENT 1 installation.

This is a **specs-only** pack — the node code lives in `app/src/`. This pack provides `node-spec.json` files that power the RAG prompt-to-workflow system.

## Nodes (32)

| Node | Category | Description |
|------|----------|-------------|
| Image Input | input | Load images from file, URL, or clipboard |
| Prompt | input | Text prompt with variables and templates |
| Annotation | input | Add notes and comments to workflow |
| Nano Banana | image/generation | AI image generation via Nano Banana API |
| LLM Generate | llm | Text generation via Gemini, Claude, GPT |
| Split Grid | image/utility | Split image into grid cells |
| Output | output | Final workflow output node |
| Generate Video | video/generation | AI video generation via Veo 3.1 |
| Generate Audio | audio/generation | AI audio/music generation |
| Generate 3D | 3d/generation | AI 3D model generation |
| Video Stitch | video/utility | Combine video clips with transitions |
| Ease Curve | video/utility | Easing curves for video transitions |
| Router | flow/routing | Route data to multiple outputs |
| Switch | flow/routing | Conditional data routing |
| Prompt Constructor | llm/utility | Build complex prompts from parts |
| Image Compare | image/utility | Side-by-side image comparison |
| Color Palette | image/utility | Extract and apply color palettes |
| Mask Editor | image/editing | Paint masks for inpainting |
| Crop & Resize | image/utility | Crop and resize images |
| Blend Mix | image/compositing | Blend multiple images |
| Text Overlay | image/compositing | Add text to images |
| Batch Process | flow/utility | Process multiple items in sequence |
| Delay | flow/utility | Add delay between operations |
| Conditional | flow/logic | If/else branching logic |
| Merge | flow/utility | Merge multiple data streams |
| Preview | output | Quick preview without saving |
| Save File | output | Save to disk with naming rules |
| API Call | integration | Generic HTTP API requests |
| JSON Parser | utility | Parse and extract JSON data |
| Variable Store | flow/state | Store and retrieve variables |
| Loop Control | flow/logic | For/while loop execution |
| Debug Log | utility | Log data for debugging |

## This pack cannot be disabled or removed.
