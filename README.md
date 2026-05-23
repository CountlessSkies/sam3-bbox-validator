# ComfyUI SAM3 BBox Validator

A custom node for ComfyUI that receives bounding box outputs (`BBOX` / `BOUNDING_BOX`) from the official **SAM3 Detect** node, runs a conditional validation check, and outputs a BOOLEAN state.

This utility node is designed to easily enable conditional branching and flow logic in ComfyUI workflows based on object detection results.

## Features
- **Highly Compatible**: Seamlessly parses SAM3's native `list[list[dict]]` data structure for single images and batch runs.
- **4 Validation Modes**:
  - `any_detected`: Returns `True` if any object is detected in any frame.
  - `min_score_detected`: Returns `True` if any detected box has a confidence score greater than or equal to `min_score`.
  - `min_area_detected`: Returns `True` if any box's area (width * height in pixels) is greater than or equal to `min_area` (perfect for filtering out small speckles/noise).
  - `count_at_least`: Returns `True` if any frame contains at least `min_count` detected objects.

## Node Inputs
- `bboxes` (Required, BOUNDING_BOX): The bounding boxes output from the SAM3 Detect node.
- `check_mode` (Required, Combo): The verification check mode to run.
- `min_score` (Required, FLOAT): The minimum confidence score threshold (default: `0.5`).
- `min_area` (Required, INT): The minimum box area in pixels (default: `0`).
- `min_count` (Required, INT): The minimum number of boxes (default: `1`).

## Node Outputs
- `boolean` (BOOLEAN): `True` or `False`.
- `int_value` (INT): `1` (for True) or `0` (for False).
- `string_value` (STRING): `"true"` or `"false"`.

## Installation
Just download or clone this repository into your `ComfyUI/custom_nodes/` folder:
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/CountlessSkies/sam3-bbox-validator.git
```
Then restart ComfyUI!
